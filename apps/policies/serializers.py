"""Serializers for policies and related provider entities."""
from __future__ import annotations

from typing import Any

from django.db import transaction
from rest_framework import serializers

from apps.clients.models import Client
from apps.lookups.models import (
    BusinessType,
    FinanceCompany,
    InsuranceType,
    PolicyStatus,
    PolicyType,
)
from apps.lookups.serializers import LookupSerializer
from apps.accounts.models import User

from .models import CarrierProduct, Coverage, GeneralAgent, Policy, PolicyFinancial, ReferralCompany


class UserSummarySerializer(serializers.ModelSerializer):
    """Lightweight representation of a user for policy responses."""

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "role")
        read_only_fields = fields


class ClientSummarySerializer(serializers.ModelSerializer):
    """Minimal client payload used when embedding policies."""

    class Meta:
        model = Client
        fields = ("id", "company_name")
        read_only_fields = fields


class GeneralAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralAgent
        fields = ("id", "name", "agency_commission", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "is_active", "created_at", "updated_at")


class CarrierProductSerializer(serializers.ModelSerializer):
    general_agent = GeneralAgentSerializer(read_only=True)
    general_agent_id = serializers.PrimaryKeyRelatedField(
        queryset=GeneralAgent.objects.filter(is_active=True),
        source="general_agent",
        write_only=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = CarrierProduct
        fields = (
            "id",
            "line_of_business",
            "general_agent",
            "general_agent_id",
            "insurance_company_name",
            "abbreviation",
            "new_business_commission_pct",
            "renewal_commission_pct",
            "is_retained",
            "is_premium_financed",
            "has_sweep_down",
            "has_sweep_payment",
            "has_auto_renew",
            "naic_code",
            "am_best_number",
            "am_best_rating",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "general_agent", "is_active", "created_at", "updated_at")


class ReferralCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCompany
        fields = ("id", "name", "rate", "is_active", "created_at", "updated_at")
        read_only_fields = ("id", "is_active", "created_at", "updated_at")


class PolicyFinancialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyFinancial
        exclude = ("policy",)
        read_only_fields = ("id", "is_active", "created_at", "updated_at")


class CoverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coverage
        fields = ("id", "coverage_type", "limits", "deductible", "is_active")
        read_only_fields = ("id", "is_active")


class PolicySerializer(serializers.ModelSerializer):
    client = ClientSummarySerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.filter(is_active=True),
        source="client",
        write_only=True,
    )
    status = LookupSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(
        queryset=PolicyStatus.objects.filter(is_active=True),
        source="status",
        write_only=True,
    )
    business_type = LookupSerializer(read_only=True)
    business_type_id = serializers.PrimaryKeyRelatedField(
        queryset=BusinessType.objects.filter(is_active=True),
        source="business_type",
        write_only=True,
    )
    insurance_type = LookupSerializer(read_only=True)
    insurance_type_id = serializers.PrimaryKeyRelatedField(
        queryset=InsuranceType.objects.filter(is_active=True),
        source="insurance_type",
        write_only=True,
    )
    policy_type = LookupSerializer(read_only=True)
    policy_type_id = serializers.PrimaryKeyRelatedField(
        queryset=PolicyType.objects.filter(is_active=True),
        source="policy_type",
        write_only=True,
    )
    carrier_product = CarrierProductSerializer(read_only=True)
    carrier_product_id = serializers.PrimaryKeyRelatedField(
        queryset=CarrierProduct.objects.filter(is_active=True),
        source="carrier_product",
        write_only=True,
    )
    finance_company = LookupSerializer(read_only=True)
    finance_company_id = serializers.PrimaryKeyRelatedField(
        queryset=FinanceCompany.objects.filter(is_active=True),
        source="finance_company",
        write_only=True,
        allow_null=True,
        required=False,
    )
    producer = UserSummarySerializer(read_only=True)
    producer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True),
        source="producer",
        write_only=True,
        allow_null=True,
        required=False,
    )
    account_manager = UserSummarySerializer(read_only=True)
    account_manager_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True),
        source="account_manager",
        write_only=True,
        allow_null=True,
        required=False,
    )
    referral_company = ReferralCompanySerializer(read_only=True)
    referral_company_id = serializers.PrimaryKeyRelatedField(
        queryset=ReferralCompany.objects.filter(is_active=True),
        source="referral_company",
        write_only=True,
        allow_null=True,
        required=False,
    )
    financials = PolicyFinancialSerializer(required=False)
    coverages = CoverageSerializer(many=True, required=False)

    class Meta:
        model = Policy
        fields = (
            "id",
            "client",
            "client_id",
            "policy_number",
            "status",
            "status_id",
            "business_type",
            "business_type_id",
            "insurance_type",
            "insurance_type_id",
            "policy_type",
            "policy_type_id",
            "effective_date",
            "maturity_date",
            "carrier_product",
            "carrier_product_id",
            "finance_company",
            "finance_company_id",
            "producer",
            "producer_id",
            "account_manager",
            "account_manager_id",
            "account_manager_rate",
            "referral_company",
            "referral_company_id",
            "financials",
            "coverages",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "client",
            "status",
            "business_type",
            "insurance_type",
            "policy_type",
            "carrier_product",
            "finance_company",
            "producer",
            "account_manager",
            "referral_company",
            "is_active",
            "created_at",
            "updated_at",
        )

    def _sync_coverages(self, policy: Policy, items: list[dict[str, Any]], *, clear_existing: bool) -> None:
        manager = policy.coverages
        existing = {str(obj.id): obj for obj in manager.all()}

        if clear_existing:
            for coverage in existing.values():
                coverage.delete()
            existing = {}

        for raw in items:
            data = dict(raw)
            coverage_id = str(data.pop("id", "") or "")
            is_active = data.pop("is_active", True)

            if coverage_id and coverage_id in existing and not clear_existing:
                obj = existing[coverage_id]
                for field in ["coverage_type", "limits", "deductible"]:
                    if field in data:
                        setattr(obj, field, data[field])
                obj.is_active = is_active
                obj.save(update_fields=["coverage_type", "limits", "deductible", "is_active", "updated_at"])
                continue

            if not data.get("coverage_type"):
                raise serializers.ValidationError("coverage_type is required for coverages.")
            manager.create(is_active=is_active, **data)

    def _upsert_financials(self, policy: Policy, payload: dict[str, Any] | None) -> None:
        if payload is None:
            return

        financials, _created = PolicyFinancial.objects.get_or_create(policy=policy)
        for field, value in payload.items():
            setattr(financials, field, value)
        financials.save()

    def create(self, validated_data: dict[str, Any]) -> Policy:
        financials_data = validated_data.pop("financials", None)
        coverages_data = validated_data.pop("coverages", [])

        with transaction.atomic():
            policy = Policy.objects.create(**validated_data)
            self._upsert_financials(policy, financials_data)
            self._sync_coverages(policy, coverages_data, clear_existing=True)
        return policy

    def update(self, instance: Policy, validated_data: dict[str, Any]) -> Policy:
        financials_data = validated_data.pop("financials", None)
        coverages_data = validated_data.pop("coverages", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        with transaction.atomic():
            instance.save()
            self._upsert_financials(instance, financials_data)
            if coverages_data is not None:
                clear = not self.partial or not coverages_data
                self._sync_coverages(instance, coverages_data, clear_existing=clear)
        return instance

    def to_internal_value(self, data: Any) -> Any:
        value = super().to_internal_value(data)

        def merge_items(raw_items, cleaned_items):
            merged: list[dict[str, Any]] = []
            for raw, cleaned in zip(raw_items, cleaned_items):
                merged_item = dict(cleaned)
                for key, val in raw.items():
                    if key.endswith("_id"):
                        continue
                    if key not in merged_item:
                        merged_item[key] = val
                merged.append(merged_item)
            return merged

        if "coverages" in data and value.get("coverages"):
            value["coverages"] = merge_items(data.get("coverages") or [], value["coverages"])
        return value
