"""API views for client endpoints."""
from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.prefetch_related(
        "dbas",
        "contacts",
        "addresses__address",
        "addresses__address_type",
    )
    serializer_class = ClientSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = {
        "dot_number": ["exact", "icontains"],
        "fein": ["exact", "icontains"],
        "contacts__contact_type": ["exact"],
        "created_by": ["exact"],
    }
    search_fields = (
        "company_name",
        "dot_number",
        "fein",
        "referral_source",
        "dbas__dba_name",
        "contacts__first_name",
        "contacts__last_name",
    )
    ordering_fields = ("company_name", "created_at", "updated_at")
    ordering = ("company_name",)

    def perform_create(self, serializer: ClientSerializer) -> None:
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer: ClientSerializer) -> None:
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance: Client) -> None:
        instance.is_active = False
        instance.updated_by = self.request.user
        instance.save(update_fields=["is_active", "updated_by", "updated_at"])
        instance.dbas.update(is_active=False)
        instance.contacts.update(is_active=False)
        instance.addresses.update(is_active=False)

    def get_queryset(self):
        queryset = super().get_queryset()
        include_inactive = self.request.query_params.get("include_inactive")
        if include_inactive not in {"true", "1", "yes"}:
            queryset = queryset.filter(is_active=True)
        return queryset.distinct()
