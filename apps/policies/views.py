"""API viewsets for the policy domain."""
from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import CarrierProduct, GeneralAgent, Policy, PolicyFinancial, ReferralCompany
from .serializers import (
    CarrierProductSerializer,
    GeneralAgentSerializer,
    PolicySerializer,
    ReferralCompanySerializer,
)


class BaseSoftDeleteViewSet(ModelViewSet):
    """Common soft-delete behaviour for policy domain viewsets."""

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset()
        include_inactive = self.request.query_params.get("include_inactive")
        if include_inactive not in {"true", "1", "yes"}:
            queryset = queryset.filter(is_active=True)
        return queryset

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])


class GeneralAgentViewSet(BaseSoftDeleteViewSet):
    queryset = GeneralAgent.objects.all()
    serializer_class = GeneralAgentSerializer
    search_fields = ("name",)
    ordering_fields = ("name", "created_at")
    ordering = ("name",)


class CarrierProductViewSet(BaseSoftDeleteViewSet):
    queryset = CarrierProduct.objects.select_related("general_agent")
    serializer_class = CarrierProductSerializer
    search_fields = ("insurance_company_name", "line_of_business", "general_agent__name")
    ordering_fields = ("insurance_company_name", "line_of_business", "created_at")
    ordering = ("insurance_company_name",)


class ReferralCompanyViewSet(BaseSoftDeleteViewSet):
    queryset = ReferralCompany.objects.all()
    serializer_class = ReferralCompanySerializer
    search_fields = ("name",)
    ordering_fields = ("name", "created_at")
    ordering = ("name",)


class PolicyViewSet(BaseSoftDeleteViewSet):
    serializer_class = PolicySerializer
    queryset = Policy.objects.select_related(
        "client",
        "status",
        "business_type",
        "insurance_type",
        "policy_type",
        "carrier_product",
        "carrier_product__general_agent",
        "finance_company",
        "producer",
        "account_manager",
        "referral_company",
    ).prefetch_related("coverages")
    filterset_fields = {
        "client": ["exact"],
        "status": ["exact"],
        "business_type": ["exact"],
        "insurance_type": ["exact"],
        "policy_type": ["exact"],
        "carrier_product": ["exact"],
        "finance_company": ["exact"],
        "producer": ["exact"],
        "account_manager": ["exact"],
        "referral_company": ["exact"],
        "effective_date": ["exact", "gte", "lte"],
    }
    search_fields = (
        "policy_number",
        "client__company_name",
        "carrier_product__insurance_company_name",
        "carrier_product__general_agent__name",
    )
    ordering_fields = (
        "policy_number",
        "effective_date",
        "maturity_date",
        "created_at",
        "updated_at",
    )
    ordering = ("-effective_date", "policy_number")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.distinct()

    def perform_create(self, serializer: PolicySerializer) -> None:
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer: PolicySerializer) -> None:
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance: Policy) -> None:
        instance.is_active = False
        instance.updated_by = self.request.user
        instance.save(update_fields=["is_active", "updated_by", "updated_at"])

        if hasattr(instance, "financials"):
            financials: PolicyFinancial = instance.financials
            financials.is_active = False
            financials.save(update_fields=["is_active", "updated_at"])

        for coverage in instance.coverages.all():
            coverage.is_active = False
            coverage.save(update_fields=["is_active", "updated_at"])
