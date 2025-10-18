"""App configuration for the policies domain."""
from __future__ import annotations

from django.apps import AppConfig


class PoliciesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.policies"
    verbose_name = "Policies"
