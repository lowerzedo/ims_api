"""API views for client endpoints."""
from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.prefetch_related("dbas", "contacts", "addresses__address", "addresses__address_type")
    serializer_class = ClientSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer: ClientSerializer) -> None:
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer: ClientSerializer) -> None:
        serializer.save(updated_by=self.request.user)

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
