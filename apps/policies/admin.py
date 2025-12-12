"""Admin configuration for policy domain models."""
from __future__ import annotations

from django.contrib import admin

from .models import CarrierProduct, Coverage, GeneralAgent, Policy, PolicyFinancial, ReferralCompany


class CoverageInline(admin.TabularInline):
    model = Coverage
    extra = 0
    fields = ("coverage_type", "limits", "deductible", "is_active", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")


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
    inlines = (CoverageInline,)
    list_display = (
        "policy_number",
        "client",
        "status",
        "producer",
        "account_manager",
        "effective_date",
        "maturity_date",
        "is_active",
    )
    search_fields = (
        "policy_number",
        "client__company_name",
        "producer__email",
        "producer__first_name",
        "producer__last_name",
        "account_manager__email",
        "account_manager__first_name",
        "account_manager__last_name",
    )
    list_filter = (
        "status",
        "business_type",
        "insurance_type",
        "policy_type",
        "producer",
        "account_manager",
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
    fieldsets = (
        (None, {"fields": ("client", "policy_number", "status")}),
        (
            "Policy Details",
            {
                "fields": (
                    "business_type",
                    "insurance_type",
                    "policy_type",
                    "carrier_product",
                    "finance_company",
                ),
            },
        ),
        (
            "Dates",
            {"fields": ("effective_date", "maturity_date")},
        ),
        (
            "Assignments & Commissions",
            {
                "fields": (
                    "producer",
                    "producer_rate",
                    "account_manager",
                    "account_manager_rate",
                    "referral_company",
                ),
                "description": "Assign producer/account manager and set their commission rates for this policy.",
            },
        ),
        (
            "Audit",
            {
                "fields": ("created_by", "updated_by", "is_active"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(Coverage)
class CoverageAdmin(admin.ModelAdmin):
    list_display = ("policy", "coverage_type", "limits", "deductible", "is_active")
    search_fields = ("policy__policy_number", "policy__client__company_name", "coverage_type", "limits")
    list_filter = ("is_active", "coverage_type")
    autocomplete_fields = ("policy",)


@admin.register(PolicyFinancial)
class PolicyFinancialAdmin(admin.ModelAdmin):
    list_display = (
        "policy",
        "original_pure_premium",
        "latest_pure_premium",
        "total_premium",
        "producer_commission_amt",
        "acct_manager_commission_amt",
        "referral_commission_amt",
        "is_active",
    )
    search_fields = ("policy__policy_number",)
    autocomplete_fields = ("policy",)
    fieldsets = (
        (None, {"fields": ("policy",)}),
        (
            "Premium",
            {
                "fields": (
                    "original_pure_premium",
                    "latest_pure_premium",
                    "broker_fee",
                    "taxes",
                    "agency_fee",
                    "total_premium",
                    "down_payment",
                ),
            },
        ),
        (
            "Commissions",
            {
                "fields": (
                    "producer_commission_amt",
                    "acct_manager_commission_amt",
                    "referral_commission_amt",
                ),
            },
        ),
    )
