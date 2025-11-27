"""Common abstract base models used across the project."""
from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Abstract model that tracks creation and update timestamps."""

    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDPrimaryKeyModel(models.Model):
    """Abstract model that uses UUID4 as the primary key."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet with helpers for soft-deletion."""

    def alive(self) -> "SoftDeleteQuerySet":
        return self.filter(is_active=True)

    def deleted(self) -> "SoftDeleteQuerySet":
        return self.filter(is_active=False)


class SoftDeleteModel(models.Model):
    """Adds a boolean flag to represent soft deletion."""

    is_active = models.BooleanField(default=True)

    objects = SoftDeleteQuerySet.as_manager()

    class Meta:
        abstract = True


class BaseModel(UUIDPrimaryKeyModel, TimeStampedModel, SoftDeleteModel):
    """Base model combining UUID, timestamps, and soft-delete semantics."""

    class Meta:
        abstract = True


class ActivityLog(UUIDPrimaryKeyModel):
    """
    Activity log tracking all changes and actions within the system.
    Used for the Timeline page to show complete history per client.
    """

    class ActionType(models.TextChoices):
        # Client actions
        CLIENT_CREATED = "client_created", "Client Created"
        CLIENT_UPDATED = "client_updated", "Client Updated"
        # Policy actions
        POLICY_CREATED = "policy_created", "Policy Created"
        POLICY_UPDATED = "policy_updated", "Policy Updated"
        POLICY_BOUND = "policy_bound", "Policy Bound"
        POLICY_CANCELLED = "policy_cancelled", "Policy Cancelled"
        # Vehicle actions
        VEHICLE_CREATED = "vehicle_created", "New Vehicle"
        VEHICLE_UPDATED = "vehicle_updated", "Edit Vehicle"
        VEHICLE_ASSIGNED = "vehicle_assigned", "Assign Vehicle"
        VEHICLE_REMOVED = "vehicle_removed", "Remove Vehicle"
        # Driver actions
        DRIVER_CREATED = "driver_created", "New Driver"
        DRIVER_UPDATED = "driver_updated", "Edit Driver"
        DRIVER_ASSIGNED = "driver_assigned", "Assign Driver"
        DRIVER_REMOVED = "driver_removed", "Remove Driver"
        # Endorsement actions
        ENDORSEMENT_CREATED = "endorsement_created", "Endorsement Created"
        ENDORSEMENT_STARTED = "endorsement_started", "Endorsement Started"
        ENDORSEMENT_COMPLETED = "endorsement_completed", "Endorsement Completed"
        ENDORSEMENT_CANCELLED = "endorsement_cancelled", "Endorsement Cancelled"
        ENDORSEMENT_UPDATED = "endorsement_updated", "Endorsement Updated"
        # Certificate actions
        CERTIFICATE_CREATED = "certificate_created", "Certificate Created"
        CERTIFICATE_UPDATED = "certificate_updated", "Certificate Updated"
        # General
        USER_ACTION = "user_action", "User Action"

    # Core fields
    action_type = models.CharField(max_length=32, choices=ActionType.choices)
    transaction_name = models.CharField(
        max_length=255,
        help_text="Display name like 'Endorsement 09/17/2025' or 'Bind'",
    )
    description = models.TextField(
        blank=True,
        help_text="Auto-generated log trail description",
    )
    notes = models.TextField(blank=True, help_text="Optional user notes")

    # Timestamps
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    # Related entities
    client = models.ForeignKey(
        "clients.Client",
        related_name="activity_logs",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    policy = models.ForeignKey(
        "policies.Policy",
        related_name="activity_logs",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    endorsement = models.ForeignKey(
        "endorsements.Endorsement",
        related_name="activity_logs",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    vehicle = models.ForeignKey(
        "assets.Vehicle",
        related_name="activity_logs",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    driver = models.ForeignKey(
        "assets.Driver",
        related_name="activity_logs",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # Who performed the action
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="activity_logs",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # Additional context stored as JSON
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ("-timestamp",)
        indexes = [
            models.Index(fields=["client", "-timestamp"]),
            models.Index(fields=["policy", "-timestamp"]),
            models.Index(fields=["action_type", "-timestamp"]),
        ]

    def __str__(self) -> str:
        return f"{self.transaction_name} - {self.get_action_type_display()}"

    @property
    def carrier_name(self) -> str | None:
        """Return carrier/insurance company name from policy."""
        if self.policy and self.policy.carrier_product:
            return self.policy.carrier_product.insurance_company_name
        return None

    @property
    def policy_number(self) -> str | None:
        """Return policy number if available."""
        if self.policy:
            return self.policy.policy_number
        return None
