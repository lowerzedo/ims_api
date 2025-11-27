"""Policy domain models covering providers, policies, and financial details."""
from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.common.models import BaseModel


class GeneralAgent(BaseModel):
    """Insurance general agency metadata managed by administrators."""

    name = models.CharField(max_length=255, unique=True)
    agency_commission = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Default commission percentage paid to the agency.",
    )

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:  # pragma: no cover - trivial representation
        return self.name


class CarrierProduct(BaseModel):
    """Carrier product offering tied to a general agent."""

    line_of_business = models.CharField(max_length=128)
    general_agent = models.ForeignKey(
        GeneralAgent,
        related_name="carrier_products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    insurance_company_name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=64, blank=True)
    new_business_commission_pct = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    renewal_commission_pct = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    is_retained = models.BooleanField(default=False)
    is_premium_financed = models.BooleanField(default=False)
    has_sweep_down = models.BooleanField(default=False)
    has_sweep_payment = models.BooleanField(default=False)
    has_auto_renew = models.BooleanField(default=False)
    naic_code = models.CharField(max_length=32, blank=True)
    am_best_number = models.CharField(max_length=32, blank=True)
    am_best_rating = models.CharField(max_length=32, blank=True)

    class Meta:
        ordering = ("insurance_company_name",)
        unique_together = ("insurance_company_name", "line_of_business")

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.insurance_company_name} - {self.line_of_business}"


class ReferralCompany(BaseModel):
    """Referral partner associated with a commission rate."""

    name = models.CharField(max_length=255, unique=True)
    rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text="Referral commission percentage applied to pure premium.",
    )

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:  # pragma: no cover
        return self.name


class Policy(BaseModel):
    """Insurance policy maintained for a client."""

    client = models.ForeignKey(
        "clients.Client",
        related_name="policies",
        on_delete=models.CASCADE,
    )
    policy_number = models.CharField(max_length=128)
    status = models.ForeignKey(
        "lookups.PolicyStatus",
        related_name="policies",
        on_delete=models.PROTECT,
    )
    business_type = models.ForeignKey(
        "lookups.BusinessType",
        related_name="policies",
        on_delete=models.PROTECT,
    )
    insurance_type = models.ForeignKey(
        "lookups.InsuranceType",
        related_name="policies",
        on_delete=models.PROTECT,
    )
    policy_type = models.ForeignKey(
        "lookups.PolicyType",
        related_name="policies",
        on_delete=models.PROTECT,
    )
    effective_date = models.DateField()
    maturity_date = models.DateField()
    carrier_product = models.ForeignKey(
        CarrierProduct,
        related_name="policies",
        on_delete=models.PROTECT,
    )
    finance_company = models.ForeignKey(
        "lookups.FinanceCompany",
        related_name="policies",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    producer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="policies_produced",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    producer_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("100.00")),
        ],
        help_text="Percentage of pure premium paid to the producer for this policy.",
    )
    account_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="policies_managed",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    account_manager_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(Decimal("0.00")),
            MaxValueValidator(Decimal("100.00")),
        ],
        help_text="Percentage of pure premium paid to the account manager for this policy.",
    )
    referral_company = models.ForeignKey(
        ReferralCompany,
        related_name="policies",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="policies_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="policies_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("-effective_date", "policy_number")
        unique_together = ("client", "policy_number")

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.policy_number} ({self.client})"


class PolicyFinancial(BaseModel):
    """Financial snapshot for a policy."""

    policy = models.OneToOneField(
        Policy,
        related_name="financials",
        on_delete=models.CASCADE,
    )
    original_pure_premium = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    latest_pure_premium = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    broker_fee = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    taxes = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    agency_fee = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    total_premium = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    down_payment = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    acct_manager_commission_amt = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    referral_commission_amt = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ("policy",)

    def __str__(self) -> str:  # pragma: no cover
        return f"Financials for {self.policy}"


class Coverage(BaseModel):
    """Coverage line stored on a policy."""

    policy = models.ForeignKey(Policy, related_name="coverages", on_delete=models.CASCADE)
    coverage_type = models.CharField(max_length=128)
    limits = models.CharField(max_length=128, blank=True)
    deductible = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ("coverage_type",)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.coverage_type} ({self.policy})"
