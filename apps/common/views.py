"""Shared API views."""
from __future__ import annotations

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):  # noqa: D401 - simple health endpoint
    """Lightweight health-check endpoint."""
    return Response({"status": "ok"})
