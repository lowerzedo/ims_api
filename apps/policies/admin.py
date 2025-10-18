"""Admin configuration for policy domain models."""
from __future__ import annotations

from django.contrib import admin

from .models import CarrierProduct, GeneralAgent, Policy, PolicyFinancial, ReferralCompany


@admin.register(GeneralAgent)
class GeneralAgentAdmin(admin.ModelAdmin):
    list_display = ("name", "agency_commission", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(CarrierProduct)
class CarrierProductAdmin(admin.ModelAdmin):
    list_display = (
        "insurance_company_name",
        "line_of_business",
        "general_agent",
        "is_active",
    )
    search_fields = (
        "insurance_company_name",
        "line_of_business",
        "general_agent__name",
    )
    list_filter = ("is_active", "general_agent")
    autocomplete_fields = ("general_agent",)


@admin.register(ReferralCompany)
class ReferralCompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "rate", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = (
        "policy_number",
        "client",
        "status",
        "effective_date",
        "maturity_date",
        "is_active",
    )
    search_fields = (
        "policy_number",
        "client__company_name",
    )
    list_filter = (
        "status",
        "business_type",
        "insurance_type",
        "policy_type",
        "is_active",
    )
    autocomplete_fields = (
        "client",
        "status",
        "business_type",
        "insurance_type",
        "policy_type",
        "carrier_product",
        "finance_company",
        "producer",
        "account_manager",
        "referral_company",
    )


@admin.register(PolicyFinancial)
class PolicyFinancialAdmin(admin.ModelAdmin):
    list_display = (
        "policy",
        "original_pure_premium",
        "latest_pure_premium",
        "broker_fee",
        "taxes",
        "agency_fee",
        "total_premium",
        "down_payment",
        "is_active",
    )
    search_fields = ("policy__policy_number",)
    autocomplete_fields = ("policy",)
