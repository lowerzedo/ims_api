"""Models implementing policy endorsement workflow."""
from __future__ import annotations

from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel


class Endorsement(BaseModel):
    """Represents a policy change workflow tracked across stages."""

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    class Stage(models.TextChoices):
        CLIENT = "client", "Client"
        VEHICLES = "vehicles", "Vehicles"
        DRIVERS = "drivers", "Drivers"
        COVERAGES = "coverages", "Coverages"
        PREMIUM = "premium", "Premium"
        FINAL = "final", "Final"

    policy = models.ForeignKey(
        "policies.Policy",
        related_name="endorsements",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=32,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    current_stage = models.CharField(
        max_length=32,
        choices=Stage.choices,
        default=Stage.CLIENT,
    )
    effective_date = models.DateField(null=True, blank=True)
    premium_change = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    fees_change = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    taxes_change = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    agency_fee_change = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    total_premium_change = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    notes = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="endorsements_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="endorsements_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:  # pragma: no cover - display helper
        return f"{self.name} ({self.policy})"

    def mark_completed(self, *, user) -> None:
        self.status = self.Status.COMPLETED
        self.current_stage = self.Stage.FINAL
        self.completed_at = timezone.now()
        self.updated_by = user
        self.save(update_fields=[
            "status",
            "current_stage",
            "completed_at",
            "updated_by",
            "updated_at",
        ])

    def mark_cancelled(self, *, user, reason: str | None = None) -> None:
        self.status = self.Status.CANCELLED
        self.current_stage = self.Stage.FINAL
        self.completed_at = timezone.now()
        if reason:
            self.notes = (self.notes + "\n" if self.notes else "") + reason.strip()
        self.updated_by = user
        self.save(update_fields=[
            "status",
            "current_stage",
            "completed_at",
            "notes",
            "updated_by",
            "updated_at",
        ])


class EndorsementChange(BaseModel):
    """Granular change captured as part of an endorsement."""

    class ChangeType(models.TextChoices):
        CLIENT = "client", "Client"
        ADDRESS = "address", "Address"
        VEHICLES = "vehicles", "Vehicles"
        DRIVERS = "drivers", "Drivers"
        COVERAGES = "coverages", "Coverages"
        PREMIUM = "premium", "Premium"
        OTHER = "other", "Other"

    endorsement = models.ForeignKey(
        Endorsement,
        related_name="changes",
        on_delete=models.CASCADE,
    )
    stage = models.CharField(
        max_length=32,
        choices=Endorsement.Stage.choices,
    )
    change_type = models.CharField(
        max_length=32,
        choices=ChangeType.choices,
    )
    summary = models.CharField(max_length=255)
    details = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="endorsement_changes",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("created_at",)

    def __str__(self) -> str:  # pragma: no cover - trivial repr
        return f"{self.get_change_type_display()} change for {self.endorsement}"
