"""Domain lookup tables shared across the system."""
from __future__ import annotations

from django.db import models

from apps.common.models import BaseModel


class LookupBase(BaseModel):
    """Common fields for lookup entities."""

    name = models.CharField(max_length=128, unique=True)

    class Meta:
        abstract = True
        ordering = ("name",)

    def __str__(self) -> str:  # pragma: no cover - trivial repr
        return self.name


class PolicyStatus(LookupBase):
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "lookup_policy_statuses"
        verbose_name = "Policy Status"
        verbose_name_plural = "Policy Statuses"


class BusinessType(LookupBase):
    class Meta:
        db_table = "lookup_business_types"
        verbose_name = "Business Type"
        verbose_name_plural = "Business Types"


class InsuranceType(LookupBase):
    class Meta:
        db_table = "lookup_insurance_types"
        verbose_name = "Insurance Type"
        verbose_name_plural = "Insurance Types"


class PolicyType(LookupBase):
    class Meta:
        db_table = "lookup_policy_types"
        verbose_name = "Policy Type"
        verbose_name_plural = "Policy Types"


class FinanceCompany(LookupBase):
    class Meta:
        db_table = "lookup_finance_companies"
        verbose_name = "Finance Company"
        verbose_name_plural = "Finance Companies"


class ContactType(LookupBase):
    class Meta:
        db_table = "lookup_contact_types"
        verbose_name = "Contact Type"
        verbose_name_plural = "Contact Types"


class AddressType(LookupBase):
    class Meta:
        db_table = "lookup_address_types"
        verbose_name = "Address Type"
        verbose_name_plural = "Address Types"


class VehicleType(LookupBase):
    class Meta:
        db_table = "lookup_vehicle_types"
        verbose_name = "Vehicle Type"
        verbose_name_plural = "Vehicle Types"


class LicenseClass(LookupBase):
    class Meta:
        db_table = "lookup_license_classes"
        verbose_name = "License Class"
        verbose_name_plural = "License Classes"


class DocumentType(LookupBase):
    class Meta:
        db_table = "lookup_document_types"
        verbose_name = "Document Type"
        verbose_name_plural = "Document Types"
