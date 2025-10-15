"""Common abstract base models used across the project."""
from __future__ import annotations

import uuid

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
