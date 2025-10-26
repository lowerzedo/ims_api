"""Admin configuration for certificates domain."""
from __future__ import annotations

from django.contrib import admin

from .models import (
    Certificate,
    CertificateDriver,
    CertificateHolder,
    CertificateVehicle,
    MasterCertificate,
)


class CertificateVehicleInline(admin.TabularInline):
    model = CertificateVehicle
    extra = 0
    autocomplete_fields = ["vehicle"]


class CertificateDriverInline(admin.TabularInline):
    model = CertificateDriver
    extra = 0
    autocomplete_fields = ["driver"]


@admin.register(CertificateHolder)
class CertificateHolderAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone_number", "contact_person", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "email", "contact_person", "phone_number")
    autocomplete_fields = ["address"]


@admin.register(MasterCertificate)
class MasterCertificateAdmin(admin.ModelAdmin):
    list_display = ("name", "policy", "is_active", "created_by", "created_at", "updated_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "policy__policy_number")
    autocomplete_fields = ["policy"]
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        if not change:  # Creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = (
        "verification_code",
        "certificate_holder",
        "master_certificate",
        "is_active",
        "created_at",
        "created_by",
    )
    list_filter = ("is_active", "created_at")
    search_fields = (
        "verification_code",
        "certificate_holder__name",
        "master_certificate__name",
        "master_certificate__policy__policy_number",
    )
    autocomplete_fields = ["master_certificate", "certificate_holder"]
    readonly_fields = ("verification_code", "created_by", "updated_by", "created_at", "updated_at")
    inlines = [CertificateVehicleInline, CertificateDriverInline]

    def save_model(self, request, obj, form, change):
        if not change:  # Creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(CertificateVehicle)
class CertificateVehicleAdmin(admin.ModelAdmin):
    list_display = ("certificate", "vehicle", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = (
        "certificate__verification_code",
        "vehicle__vin",
        "vehicle__unit_number",
    )
    autocomplete_fields = ["certificate", "vehicle"]


@admin.register(CertificateDriver)
class CertificateDriverAdmin(admin.ModelAdmin):
    list_display = ("certificate", "driver", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = (
        "certificate__verification_code",
        "driver__first_name",
        "driver__last_name",
        "driver__license_number",
    )
    autocomplete_fields = ["certificate", "driver"]
