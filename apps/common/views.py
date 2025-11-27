"""Shared API views."""
from __future__ import annotations

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import ActivityLog
from .serializers import ActivityLogCreateSerializer, ActivityLogSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):  # noqa: D401 - simple health endpoint
    """Lightweight health-check endpoint."""
    return Response({"status": "ok"})


class ActivityLogViewSet(ModelViewSet):
    """
    ViewSet for activity logs (Timeline).

    Provides complete history of all actions per client including:
    - Client creation/updates
    - Policy creation/updates
    - Vehicle/driver additions and assignments
    - Endorsement lifecycle (created, started, completed, cancelled)
    - Certificate generation
    """

    permission_classes = (IsAuthenticated,)
    filterset_fields = {
        "client": ["exact"],
        "policy": ["exact"],
        "endorsement": ["exact"],
        "action_type": ["exact", "in"],
        "performed_by": ["exact"],
        "timestamp": ["exact", "gte", "lte", "date"],
    }
    search_fields = (
        "transaction_name",
        "description",
        "notes",
        "policy__policy_number",
        "client__company_name",
        "vehicle__vin",
        "driver__first_name",
        "driver__last_name",
    )
    ordering_fields = (
        "timestamp",
        "action_type",
        "transaction_name",
    )
    ordering = ("-timestamp",)

    def get_queryset(self):
        return ActivityLog.objects.select_related(
            "client",
            "policy",
            "policy__carrier_product",
            "endorsement",
            "vehicle",
            "driver",
            "performed_by",
        )

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return ActivityLogCreateSerializer
        return ActivityLogSerializer

    def perform_create(self, serializer):
        serializer.save(performed_by=self.request.user)
