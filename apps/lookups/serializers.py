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


class LookupSerializer(serializers.Serializer):
    """Base serializer exposing the common lookup fields."""

    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)


class PolicyStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyStatus
        fields = ("id", "name", "is_active", "description")
        read_only_fields = fields


class BusinessTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessType
        fields = ("id", "name", "is_active")
        read_only_fields = fields


class InsuranceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceType
        fields = ("id", "name", "is_active")
        read_only_fields = fields


class PolicyTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyType
        fields = ("id", "name", "is_active")
        read_only_fields = fields


class FinanceCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceCompany
        fields = ("id", "name", "is_active")
        read_only_fields = fields


class ContactTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactType
        fields = ("id", "name", "is_active")
        read_only_fields = fields


class AddressTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressType
        fields = ("id", "name", "is_active")
        read_only_fields = fields


class VehicleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleType
        fields = ("id", "name", "is_active")
        read_only_fields = fields


class LicenseClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = LicenseClass
        fields = ("id", "name", "is_active")
        read_only_fields = fields


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = ("id", "name", "is_active")
        read_only_fields = fields
