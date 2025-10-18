"""Asset domain models covering vehicles and related loss payees."""
from __future__ import annotations

from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models

from apps.common.models import BaseModel


class LossPayee(BaseModel):
    """Entity with a financial interest in a vehicle."""

    class Preference(models.TextChoices):
        EMAIL = "EMAIL", "Email"
        FAX = "FAX", "Fax"

    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    contact_person_name = models.CharField(max_length=255, blank=True)
    telephone = models.CharField(max_length=32, blank=True)
    fax = models.CharField(max_length=32, blank=True)
    cell_phone = models.CharField(max_length=32, blank=True)
    preference = models.CharField(
        max_length=16,
        choices=Preference.choices,
        default=Preference.EMAIL,
    )
    remarks = models.TextField(blank=True)
    address = models.ForeignKey(
        "clients.Address",
        related_name="loss_payees",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:  # pragma: no cover - trivial repr
        return self.name


class Vehicle(BaseModel):
    """Client-owned vehicle tracked for policy assignments."""

    VIN_VALIDATOR = RegexValidator(
        regex=r"^[A-HJ-NPR-Z0-9]{17}$",
        message="VIN must be 17 characters and exclude I, O, Q.",
    )

    client = models.ForeignKey(
        "clients.Client",
        related_name="vehicles",
        on_delete=models.CASCADE,
    )
    vin = models.CharField(max_length=17, unique=True, validators=[VIN_VALIDATOR])
    unit_number = models.CharField(max_length=64, blank=True)
    vehicle_type = models.ForeignKey(
        "lookups.VehicleType",
        related_name="vehicles",
        on_delete=models.PROTECT,
    )
    year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
    )
    make = models.CharField(max_length=128)
    model = models.CharField(max_length=128)
    gvw = models.PositiveIntegerField(
        verbose_name="Gross Vehicle Weight",
        null=True,
        blank=True,
    )
    pd_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Physical damage value.",
    )
    deductible = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )
    loss_payee = models.ForeignKey(
        LossPayee,
        related_name="vehicles",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("unit_number", "vin")

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.unit_number or self.vin}"


class PolicyVehicle(BaseModel):
    """Join table assigning vehicles to policies."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        UNASSIGNED = "unassigned", "Unassigned"

    policy = models.ForeignKey(
        "policies.Policy",
        related_name="policy_vehicles",
        on_delete=models.CASCADE,
    )
    vehicle = models.ForeignKey(
        Vehicle,
        related_name="policy_assignments",
        on_delete=models.CASCADE,
    )
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)
    inception_date = models.DateField(null=True, blank=True)
    termination_date = models.DateField(null=True, blank=True)
    garaging_address = models.ForeignKey(
        "clients.Address",
        related_name="policy_vehicle_garaging",
        on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = ("policy", "vehicle")
        ordering = ("policy", "vehicle")

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.policy} -> {self.vehicle}"


class Driver(BaseModel):
    """Client driver record used for assignments and compliance."""

    client = models.ForeignKey(
        "clients.Client",
        related_name="drivers",
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField()
    license_number = models.CharField(max_length=64)
    license_state = models.CharField(max_length=2)
    license_class = models.ForeignKey(
        "lookups.LicenseClass",
        related_name="drivers",
        on_delete=models.PROTECT,
    )
    issue_date = models.DateField(null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    violations = models.PositiveSmallIntegerField(default=0)
    accidents = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("last_name", "first_name")
        unique_together = ("client", "license_number")

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.first_name} {self.last_name}".strip()


class PolicyDriver(BaseModel):
    """Assignment of drivers to policies."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        NOT_ASSIGNED = "not_assigned", "Not Assigned"

    policy = models.ForeignKey(
        "policies.Policy",
        related_name="policy_drivers",
        on_delete=models.CASCADE,
    )
    driver = models.ForeignKey(
        Driver,
        related_name="policy_assignments",
        on_delete=models.CASCADE,
    )
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        unique_together = ("policy", "driver")
        ordering = ("policy", "driver")

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.policy} -> {self.driver}"
