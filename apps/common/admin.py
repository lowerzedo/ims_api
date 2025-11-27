"""Admin registrations for shared models."""
from __future__ import annotations

from django.contrib import admin

from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    """Admin for viewing activity logs (Timeline)."""

    list_display = (
        "transaction_name",
        "action_type",
        "client",
        "policy_number",
        "performed_by",
        "timestamp",
    )
    list_filter = (
        "action_type",
        "timestamp",
    )
    search_fields = (
        "transaction_name",
        "description",
        "notes",
        "client__company_name",
        "policy__policy_number",
        "vehicle__vin",
        "driver__first_name",
        "driver__last_name",
        "performed_by__email",
        "performed_by__first_name",
        "performed_by__last_name",
    )
    readonly_fields = (
        "id",
        "action_type",
        "transaction_name",
        "description",
        "notes",
        "timestamp",
        "client",
        "policy",
        "endorsement",
        "vehicle",
        "driver",
        "performed_by",
        "metadata",
        "carrier_name",
        "policy_number",
    )
    autocomplete_fields = ()
    ordering = ("-timestamp",)
    date_hierarchy = "timestamp"

    def has_add_permission(self, request):
        """Disable adding logs manually - they should be created by the system."""
        return False

    def has_change_permission(self, request, obj=None):
        """Disable editing logs - they are immutable."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disable deleting logs - they are audit records."""
        return False
