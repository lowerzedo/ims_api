"""Admin configuration for asset and vehicle models."""
from __future__ import annotations

from django.contrib import admin

from .models import Driver, LossPayee, PolicyDriver, PolicyVehicle, Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "vin",
        "unit_number",
        "client",
        "vehicle_type",
        "year",
        "make",
        "model",
        "is_active",
    )
    list_filter = ("vehicle_type", "year", "is_active")
    search_fields = (
        "vin",
        "unit_number",
        "client__company_name",
        "make",
        "model",
    )
    autocomplete_fields = ("client", "vehicle_type", "loss_payee")
    ordering = ("unit_number", "vin")


@admin.register(LossPayee)
class LossPayeeAdmin(admin.ModelAdmin):
    list_display = ("name", "preference", "address", "is_active")
    list_filter = ("preference", "is_active")
    search_fields = (
        "name",
        "address__street_address",
        "address__city",
        "address__state",
    )
    autocomplete_fields = ("address",)


@admin.register(PolicyVehicle)
class PolicyVehicleAdmin(admin.ModelAdmin):
    list_display = (
        "policy",
        "vehicle",
        "status",
        "garaging_address",
        "inception_date",
        "termination_date",
        "is_active",
    )
    list_filter = ("status", "is_active")
    search_fields = (
        "policy__policy_number",
        "vehicle__vin",
        "vehicle__unit_number",
        "garaging_address__street_address",
    )
    autocomplete_fields = ("policy", "vehicle", "garaging_address")


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "client",
        "license_number",
        "license_state",
        "license_class",
        "is_active",
    )
    list_filter = ("license_class", "license_state", "is_active")
    search_fields = (
        "first_name",
        "last_name",
        "client__company_name",
        "license_number",
    )
    autocomplete_fields = ("client", "license_class")


@admin.register(PolicyDriver)
class PolicyDriverAdmin(admin.ModelAdmin):
    list_display = ("policy", "driver", "status", "is_active")
    list_filter = ("status", "is_active")
    search_fields = (
        "policy__policy_number",
        "driver__first_name",
        "driver__last_name",
        "driver__license_number",
    )
    autocomplete_fields = ("policy", "driver")
