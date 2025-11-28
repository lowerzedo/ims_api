"""API views for client endpoints."""
from __future__ import annotations

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Address, Client
from .serializers import AddressSerializer, ClientSerializer


class AddressViewSet(ModelViewSet):
    """CRUD operations for standalone addresses (e.g., garaging addresses)."""

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)
    search_fields = ("street_address", "city", "state", "zip_code")
    ordering_fields = ("street_address", "city", "state", "created_at")
    ordering = ("street_address",)

    def get_queryset(self):
        queryset = super().get_queryset()
        include_inactive = self.request.query_params.get("include_inactive")
        if include_inactive not in {"true", "1", "yes"}:
            queryset = queryset.filter(is_active=True)
        return queryset

    def perform_destroy(self, instance: Address) -> None:
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])


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

    @action(detail=True, methods=["get"], url_path="garaging-addresses")
    def garaging_addresses(self, request, pk=None):
        """Return all garaging addresses associated with this client's vehicles."""
        client = self.get_object()
        
        # Get addresses directly attached to vehicles
        vehicle_addresses = Address.objects.filter(
            vehicles__client=client,
            vehicles__is_active=True,
            is_active=True,
        ).distinct()
        
        # Get addresses from policy vehicle assignments
        policy_vehicle_addresses = Address.objects.filter(
            policy_vehicle_garaging__vehicle__client=client,
            policy_vehicle_garaging__is_active=True,
            is_active=True,
        ).distinct()
        
        # Combine and deduplicate
        all_addresses = (vehicle_addresses | policy_vehicle_addresses).distinct()
        
        serializer = AddressSerializer(all_addresses, many=True)
        return Response(serializer.data)
