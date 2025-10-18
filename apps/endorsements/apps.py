"""Config for endorsements app."""
from __future__ import annotations

from django.apps import AppConfig


class EndorsementsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.endorsements"
    verbose_name = "Endorsements"
