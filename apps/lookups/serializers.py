"""Serializers for lookup tables."""
from __future__ import annotations

from rest_framework import serializers

from .models import (
    AddressType,
    BusinessType,
    ContactType,
    DocumentType,
    FinanceCompany,
    InsuranceType,
    LicenseClass,
    PolicyStatus,
    PolicyType,
    VehicleType,
)


class LookupSerializer(serializers.ModelSerializer):
    """Base serializer exposing the common lookup fields."""

    class Meta:
        fields = ("id", "name", "is_active")
        read_only_fields = fields


class PolicyStatusSerializer(LookupSerializer):
    class Meta(LookupSerializer.Meta):
        model = PolicyStatus
        fields = LookupSerializer.Meta.fields + ("description",)
        read_only_fields = fields


class BusinessTypeSerializer(LookupSerializer):
    class Meta(LookupSerializer.Meta):
        model = BusinessType


class InsuranceTypeSerializer(LookupSerializer):
    class Meta(LookupSerializer.Meta):
        model = InsuranceType


class PolicyTypeSerializer(LookupSerializer):
    class Meta(LookupSerializer.Meta):
        model = PolicyType


class FinanceCompanySerializer(LookupSerializer):
    class Meta(LookupSerializer.Meta):
        model = FinanceCompany


class ContactTypeSerializer(LookupSerializer):
    class Meta(LookupSerializer.Meta):
        model = ContactType


class AddressTypeSerializer(LookupSerializer):
    class Meta(LookupSerializer.Meta):
        model = AddressType


class VehicleTypeSerializer(LookupSerializer):
    class Meta(LookupSerializer.Meta):
        model = VehicleType


class LicenseClassSerializer(LookupSerializer):
    class Meta(LookupSerializer.Meta):
        model = LicenseClass


class DocumentTypeSerializer(LookupSerializer):
    class Meta(LookupSerializer.Meta):
        model = DocumentType
