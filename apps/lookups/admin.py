"""Admin configuration for lookup tables."""
from __future__ import annotations

from django.contrib import admin

from .models import (
    AddressType,
    BusinessType,
    ContactType,
    DocumentType,
    FinanceCompany,
    InsuranceType,
    LicenseClass,
    PolicyStatus,
    PolicyType,
    VehicleType,
)


@admin.register(
    PolicyStatus,
    BusinessType,
    InsuranceType,
    PolicyType,
    FinanceCompany,
    ContactType,
    AddressType,
    VehicleType,
    LicenseClass,
    DocumentType,
)
class LookupAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("name",)
