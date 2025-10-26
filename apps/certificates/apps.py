"""App configuration for certificates domain."""
from __future__ import annotations

from django.apps import AppConfig


class CertificatesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.certificates"
    verbose_name = "Certificates"
