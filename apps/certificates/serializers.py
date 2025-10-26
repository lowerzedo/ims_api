"""Serializers for the certificate domain."""
from __future__ import annotations

from typing import Any

from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import serializers

from apps.accounts.models import User
from apps.assets.models import Driver, Vehicle
from apps.clients.models import Address
from apps.clients.serializers import AddressSerializer
from apps.policies.models import Policy

from .models import Certificate, CertificateHolder, MasterCertificate
from .services import render_certificate_pdf


class UserSummarySerializer(serializers.ModelSerializer):
    """Minimal representation of a user for audit fields."""

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "role")
        read_only_fields = fields


class CertificateHolderSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = CertificateHolder
        fields = (
            "id",
            "name",
            "email",
            "contact_person",
            "phone_number",
            "address",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "is_active", "created_at", "updated_at")

    def create(self, validated_data: dict[str, Any]) -> CertificateHolder:
        address_payload = validated_data.pop("address")
        address = Address.objects.create(**address_payload)
        return CertificateHolder.objects.create(address=address, **validated_data)

    def update(self, instance: CertificateHolder, validated_data: dict[str, Any]) -> CertificateHolder:
        address_payload = validated_data.pop("address", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        with transaction.atomic():
            instance.save()
            if address_payload:
                address = instance.address
                for field, value in address_payload.items():
                    setattr(address, field, value)
                address.save(update_fields=["street_address", "city", "state", "zip_code", "updated_at"])
        return instance


class PolicySummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Policy
        fields = ("id", "policy_number")
        read_only_fields = fields


class MasterCertificateSerializer(serializers.ModelSerializer):
    policy = PolicySummarySerializer(read_only=True)
    policy_id = serializers.PrimaryKeyRelatedField(
        queryset=Policy.objects.filter(is_active=True),
        source="policy",
        write_only=True,
    )
    created_by = UserSummarySerializer(read_only=True)
    updated_by = UserSummarySerializer(read_only=True)

    class Meta:
        model = MasterCertificate
        fields = (
            "id",
            "policy",
            "policy_id",
            "name",
            "settings",
            "created_by",
            "updated_by",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "policy",
            "created_by",
            "updated_by",
            "is_active",
            "created_at",
            "updated_at",
        )


class VehicleSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ("id", "vin", "unit_number", "year", "make", "model", "pd_amount")
        read_only_fields = fields


class DriverSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = (
            "id",
            "first_name",
            "last_name",
            "license_number",
            "license_state",
            "hire_date",
        )
        read_only_fields = fields


class CertificateSerializer(serializers.ModelSerializer):
    master_certificate = MasterCertificateSerializer(read_only=True)
    master_certificate_id = serializers.PrimaryKeyRelatedField(
        queryset=MasterCertificate.objects.filter(is_active=True),
        source="master_certificate",
        write_only=True,
    )
    certificate_holder = CertificateHolderSerializer(read_only=True)
    certificate_holder_id = serializers.PrimaryKeyRelatedField(
        queryset=CertificateHolder.objects.filter(is_active=True),
        source="certificate_holder",
        write_only=True,
    )
    vehicles = VehicleSummarySerializer(many=True, read_only=True)
    vehicle_ids = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.filter(is_active=True),
        many=True,
        write_only=True,
        required=False,
    )
    drivers = DriverSummarySerializer(many=True, read_only=True)
    driver_ids = serializers.PrimaryKeyRelatedField(
        queryset=Driver.objects.filter(is_active=True),
        many=True,
        write_only=True,
        required=False,
    )
    created_by = UserSummarySerializer(read_only=True)
    updated_by = UserSummarySerializer(read_only=True)
    document = serializers.FileField(read_only=True)

    class Meta:
        model = Certificate
        fields = (
            "id",
            "master_certificate",
            "master_certificate_id",
            "certificate_holder",
            "certificate_holder_id",
            "verification_code",
            "document",
            "vehicles",
            "vehicle_ids",
            "drivers",
            "driver_ids",
            "created_by",
            "updated_by",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "master_certificate",
            "certificate_holder",
            "verification_code",
            "document",
            "vehicles",
            "drivers",
            "created_by",
            "updated_by",
            "is_active",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        master = attrs.get("master_certificate") or getattr(self.instance, "master_certificate", None)
        vehicles = attrs.get("vehicle_ids", [])
        drivers = attrs.get("driver_ids", [])

        if master is not None:
            policy = master.policy
            for vehicle in vehicles:
                if vehicle.client_id != policy.client_id:
                    raise serializers.ValidationError("Selected vehicle does not belong to the policy client.")
            for driver in drivers:
                if driver.client_id != policy.client_id:
                    raise serializers.ValidationError("Selected driver does not belong to the policy client.")
        return attrs

    def create(self, validated_data: dict[str, Any]) -> Certificate:
        vehicle_objects = validated_data.pop("vehicle_ids", [])
        driver_objects = validated_data.pop("driver_ids", [])

        with transaction.atomic():
            certificate = Certificate.objects.create(**validated_data)
            if vehicle_objects:
                certificate.vehicles.set(vehicle_objects)
            if driver_objects:
                certificate.drivers.set(driver_objects)
            self._refresh_document(certificate)
        return certificate

    def update(self, instance: Certificate, validated_data: dict[str, Any]) -> Certificate:
        vehicle_objects = validated_data.pop("vehicle_ids", None)
        driver_objects = validated_data.pop("driver_ids", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        with transaction.atomic():
            instance.save()
            if vehicle_objects is not None:
                instance.vehicles.set(vehicle_objects)
            if driver_objects is not None:
                instance.drivers.set(driver_objects)
            self._refresh_document(instance)
        return instance

    def _refresh_document(self, certificate: Certificate) -> None:
        vehicles = list(certificate.vehicles.select_related("client").all())
        drivers = list(certificate.drivers.select_related("client").all())
        payload = render_certificate_pdf(certificate, vehicles=vehicles, drivers=drivers)
        if certificate.document:
            certificate.document.delete(save=False)
        filename = f"certificate-{certificate.verification_code}.pdf"
        certificate.document.save(filename, ContentFile(payload), save=False)
        certificate.save(update_fields=["document", "updated_at"])
