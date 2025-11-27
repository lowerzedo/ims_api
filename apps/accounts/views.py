"""API views for accounts domain."""
from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import User
from .serializers import EmployeeSerializer


class EmployeeViewSet(ReadOnlyModelViewSet):
    """
    Read-only viewset for employees (users with commission rates).
    
    Returns producers and account managers who can earn commissions.
    """

    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = {
        "role": ["exact"],
        "is_active": ["exact"],
    }
    search_fields = ("email", "first_name", "last_name")
    ordering_fields = ("last_name", "first_name", "email", "date_joined")
    ordering = ("last_name", "first_name")

    def get_queryset(self):
        """Return only employees who can have commissions (producers and account managers)."""
        queryset = User.objects.filter(
            role__in=[User.Role.PRODUCER, User.Role.ACCOUNT_MANAGER],
            is_active=True,
        )
        
        # Allow filtering inactive if requested
        include_inactive = self.request.query_params.get("include_inactive")
        if include_inactive in {"true", "1", "yes"}:
            queryset = User.objects.filter(
                role__in=[User.Role.PRODUCER, User.Role.ACCOUNT_MANAGER],
            )
        
        return queryset

