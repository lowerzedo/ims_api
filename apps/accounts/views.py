"""API views for accounts domain."""
from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import User
from .serializers import EmployeeSerializer


class EmployeeViewSet(ReadOnlyModelViewSet):
    """
    Read-only viewset for employees (users who can be assigned to policies).
    
    Returns users who can be producers and/or account managers.
    Filter by capability using ?can_produce=true or ?can_manage_accounts=true
    """

    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = {
        "role": ["exact"],
        "can_produce": ["exact"],
        "can_manage_accounts": ["exact"],
        "is_active": ["exact"],
    }
    search_fields = ("email", "first_name", "last_name")
    ordering_fields = ("last_name", "first_name", "email", "date_joined")
    ordering = ("last_name", "first_name")

    def get_queryset(self):
        """Return employees who can be assigned to policies (producers or account managers)."""
        from django.db.models import Q
        
        # Base: users with any capability (can_produce OR can_manage_accounts)
        # Also include legacy role-based users for backwards compatibility
        queryset = User.objects.filter(
            Q(can_produce=True) | 
            Q(can_manage_accounts=True) |
            Q(role__in=[User.Role.PRODUCER, User.Role.ACCOUNT_MANAGER])
        ).exclude(is_superuser=True)
        
        # Filter by active status
        include_inactive = self.request.query_params.get("include_inactive")
        if include_inactive not in {"true", "1", "yes"}:
            queryset = queryset.filter(is_active=True)
        
        return queryset.distinct()

