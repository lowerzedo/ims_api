"""Certificate of Insurance domain models."""
from __future__ import annotations

from pathlib import PurePosixPath

from django.conf import settings as django_settings
from django.db import models
from django.utils.crypto import get_random_string

from apps.common.models import BaseModel


def certificate_document_upload_to(instance: "Certificate", filename: str) -> str:
    """Store generated certificates grouped by client and policy."""

    master = instance.master_certificate
    policy = master.policy
    client_id = getattr(policy.client, "id", "unknown-client")
    certificate_id = getattr(instance, "id", "pending")
    safe_path = PurePosixPath(
        "certificates",
        str(client_id),
        str(policy.id),
        str(certificate_id),
        filename,
    )
    return str(safe_path)


class CertificateHolder(BaseModel):
    """Entity that receives certificates (e.g. loss payee or additional insured)."""

    name = models.CharField(max_length=255)
    address = models.ForeignKey(
        "clients.Address",
        related_name="certificate_holders",
        on_delete=models.PROTECT,
    )
    email = models.EmailField(blank=True)
    contact_person = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=32, blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:  # pragma: no cover - formatting helper
        return self.name


class MasterCertificate(BaseModel):
    """Reusable template that drives generated certificates for a policy."""

    policy = models.ForeignKey(
        "policies.Policy",
        related_name="master_certificates",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    settings = models.JSONField(default=dict, blank=True)
    created_by = models.ForeignKey(
        django_settings.AUTH_USER_MODEL,
        related_name="master_certificates_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        django_settings.AUTH_USER_MODEL,
        related_name="master_certificates_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("name",)
        unique_together = ("policy", "name")

    def __str__(self) -> str:  # pragma: no cover - formatting helper
        return f"{self.name} ({self.policy})"


class Certificate(BaseModel):
    """Issued certificate of insurance derived from a master template."""

    master_certificate = models.ForeignKey(
        MasterCertificate,
        related_name="certificates",
        on_delete=models.CASCADE,
    )
    certificate_holder = models.ForeignKey(
        CertificateHolder,
        related_name="certificates",
        on_delete=models.PROTECT,
    )
    verification_code = models.CharField(max_length=20, unique=True, editable=False)
    document = models.FileField(
        upload_to=certificate_document_upload_to,
        max_length=512,
        blank=True,
        null=True,
    )
    created_by = models.ForeignKey(
        django_settings.AUTH_USER_MODEL,
        related_name="certificates_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        django_settings.AUTH_USER_MODEL,
        related_name="certificates_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    vehicles = models.ManyToManyField(
        "assets.Vehicle",
        through="CertificateVehicle",
        related_name="certificates",
        blank=True,
    )
    drivers = models.ManyToManyField(
        "assets.Driver",
        through="CertificateDriver",
        related_name="certificates",
        blank=True,
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:  # pragma: no cover - formatting helper
        return f"Certificate {self.verification_code}"

    def save(self, *args, **kwargs):
        if not self.verification_code:
            self.verification_code = self._generate_verification_code()
        super().save(*args, **kwargs)

    def _generate_verification_code(self) -> str:
        candidate_length = 12
        while True:
            candidate = get_random_string(candidate_length).upper()
            if not type(self).objects.filter(verification_code=candidate).exists():
                return candidate


class CertificateVehicle(BaseModel):
    """Association of a certificate with a covered vehicle."""

    certificate = models.ForeignKey(
        Certificate,
        related_name="certificate_vehicles",
        on_delete=models.CASCADE,
    )
    vehicle = models.ForeignKey(
        "assets.Vehicle",
        related_name="vehicle_certificates",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("certificate", "vehicle")
        ordering = ("certificate", "vehicle")

    def __str__(self) -> str:  # pragma: no cover - formatting helper
        return f"{self.certificate} -> {self.vehicle}"


class CertificateDriver(BaseModel):
    """Association of a certificate with a listed driver."""

    certificate = models.ForeignKey(
        Certificate,
        related_name="certificate_drivers",
        on_delete=models.CASCADE,
    )
    driver = models.ForeignKey(
        "assets.Driver",
        related_name="driver_certificates",
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ("certificate", "driver")
        ordering = ("certificate", "driver")

    def __str__(self) -> str:  # pragma: no cover - formatting helper
        return f"{self.certificate} -> {self.driver}"
