"""API viewsets for certificates domain."""
from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Certificate, CertificateHolder, MasterCertificate
from .serializers import (
    CertificateHolderSerializer,
    CertificateSerializer,
    MasterCertificateSerializer,
)


class BaseSoftDeleteViewSet(ModelViewSet):
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


class CertificateHolderViewSet(BaseSoftDeleteViewSet):
    queryset = CertificateHolder.objects.select_related("address")
    serializer_class = CertificateHolderSerializer
    search_fields = ("name", "contact_person", "address__city", "address__state")
    ordering_fields = ("name", "created_at")
    ordering = ("name",)


class MasterCertificateViewSet(BaseSoftDeleteViewSet):
    queryset = MasterCertificate.objects.select_related(
        "policy",
        "policy__client",
        "created_by",
        "updated_by",
    )
    serializer_class = MasterCertificateSerializer
    filterset_fields = {"policy": ["exact"]}
    search_fields = ("name", "policy__policy_number", "policy__client__company_name")
    ordering_fields = ("name", "created_at", "updated_at")
    ordering = ("name",)

    def perform_create(self, serializer: MasterCertificateSerializer) -> None:
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(created_by=user, updated_by=user)

    def perform_update(self, serializer: MasterCertificateSerializer) -> None:
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(updated_by=user)


class CertificateViewSet(BaseSoftDeleteViewSet):
    queryset = Certificate.objects.select_related(
        "master_certificate",
        "master_certificate__policy",
        "master_certificate__policy__client",
        "certificate_holder",
        "certificate_holder__address",
        "created_by",
        "updated_by",
    ).prefetch_related("vehicles", "drivers")
    serializer_class = CertificateSerializer
    filterset_fields = {
        "master_certificate": ["exact"],
        "master_certificate__policy": ["exact"],
        "certificate_holder": ["exact"],
    }
    search_fields = (
        "verification_code",
        "master_certificate__name",
        "master_certificate__policy__policy_number",
        "certificate_holder__name",
    )
    ordering_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    def perform_create(self, serializer: CertificateSerializer) -> None:
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(created_by=user, updated_by=user)

    def perform_update(self, serializer: CertificateSerializer) -> None:
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(updated_by=user)
