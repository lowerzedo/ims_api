"""Client domain models."""
from __future__ import annotations

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.common.models import BaseModel


class Client(BaseModel):
    company_name = models.CharField(max_length=255)
    dot_number = models.CharField(max_length=32, blank=True)
    fein = models.CharField(max_length=32, blank=True)
    date_of_authority = models.DateField(null=True, blank=True)
    referral_source = models.CharField(max_length=255, blank=True)
    factoring_company = models.CharField(max_length=255, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="clients_created",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="clients_updated",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("company_name",)

    def __str__(self) -> str:  # pragma: no cover - trivial formatting
        return self.company_name


class ClientDBA(BaseModel):
    client = models.ForeignKey(Client, related_name="dbas", on_delete=models.CASCADE)
    dba_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ("client", "dba_name")
        ordering = ("dba_name",)

    def __str__(self) -> str:  # pragma: no cover
        return self.dba_name


class Contact(BaseModel):
    client = models.ForeignKey(Client, related_name="contacts", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=32, blank=True)
    contact_type = models.ForeignKey(
        "lookups.ContactType",
        related_name="contacts",
        on_delete=models.PROTECT,
    )
    nickname = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ("first_name", "last_name")

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.first_name} {self.last_name}".strip()


class Address(BaseModel):
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=128)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10)

    class Meta:
        ordering = ("street_address",)

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.street_address}, {self.city}, {self.state} {self.zip_code}"


class ClientAddress(BaseModel):
    client = models.ForeignKey(Client, related_name="addresses", on_delete=models.CASCADE)
    address = models.ForeignKey(Address, related_name="client_links", on_delete=models.CASCADE)
    address_type = models.ForeignKey(
        "lookups.AddressType",
        related_name="client_addresses",
        on_delete=models.PROTECT,
    )
    rating = models.SmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1-5 rating used for Garaging addresses.",
    )

    class Meta:
        unique_together = ("client", "address", "address_type")
        verbose_name = "Client Address"
        verbose_name_plural = "Client Addresses"

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.client} - {self.address_type.name}"
