"""Serializers for vehicles, loss payees, and policy assignments."""
from __future__ import annotations

from typing import Any

from django.db import transaction
from rest_framework import serializers

from apps.clients.models import Address, Client
from apps.clients.serializers import AddressSerializer
from apps.lookups.models import LicenseClass, VehicleType
from apps.lookups.serializers import LookupSerializer
from apps.policies.models import Policy

from .models import Driver, LossPayee, PolicyDriver, PolicyVehicle, Vehicle


class LossPayeeSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = LossPayee
        fields = (
            "id",
            "name",
            "email",
            "contact_person_name",
            "telephone",
            "fax",
            "cell_phone",
            "preference",
            "remarks",
            "address",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "is_active", "created_at", "updated_at")

    def create(self, validated_data: dict[str, Any]) -> LossPayee:
        address_data = validated_data.pop("address")
        with transaction.atomic():
            address = Address.objects.create(**address_data)
            return LossPayee.objects.create(address=address, **validated_data)

    def update(self, instance: LossPayee, validated_data: dict[str, Any]) -> LossPayee:
        address_data = validated_data.pop("address", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        with transaction.atomic():
            instance.save()
            if address_data:
                address = instance.address
                for field, value in address_data.items():
                    setattr(address, field, value)
                address.save(update_fields=["street_address", "city", "state", "zip_code", "updated_at"])
        return instance


class ClientSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ("id", "company_name")
        read_only_fields = fields


class VehicleSerializer(serializers.ModelSerializer):
    client = ClientSummarySerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.filter(is_active=True),
        source="client",
        write_only=True,
    )
    vehicle_type = LookupSerializer(read_only=True)
    vehicle_type_id = serializers.PrimaryKeyRelatedField(
        queryset=VehicleType.objects.filter(is_active=True),
        source="vehicle_type",
        write_only=True,
    )
    loss_payee = LossPayeeSerializer(read_only=True)
    loss_payee_id = serializers.PrimaryKeyRelatedField(
        queryset=LossPayee.objects.filter(is_active=True),
        source="loss_payee",
        write_only=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Vehicle
        fields = (
            "id",
            "client",
            "client_id",
            "vin",
            "unit_number",
            "vehicle_type",
            "vehicle_type_id",
            "year",
            "make",
            "model",
            "gvw",
            "pd_amount",
            "deductible",
            "loss_payee",
            "loss_payee_id",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "client",
            "vehicle_type",
            "loss_payee",
            "is_active",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data: dict[str, Any]) -> Vehicle:
        return Vehicle.objects.create(**validated_data)

    def update(self, instance: Vehicle, validated_data: dict[str, Any]) -> Vehicle:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PolicyVehicleSerializer(serializers.ModelSerializer):
    policy = serializers.UUIDField(source="policy.id", read_only=True)
    policy_id = serializers.PrimaryKeyRelatedField(
        queryset=Policy.objects.filter(is_active=True),
        source="policy",
        write_only=True,
    )
    vehicle = VehicleSerializer(read_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.filter(is_active=True),
        source="vehicle",
        write_only=True,
    )
    garaging_address = AddressSerializer(read_only=True)
    garaging_address_id = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.filter(is_active=True),
        source="garaging_address",
        write_only=True,
    )

    class Meta:
        model = PolicyVehicle
        fields = (
            "id",
            "policy",
            "policy_id",
            "vehicle",
            "vehicle_id",
            "status",
            "inception_date",
            "termination_date",
            "garaging_address",
            "garaging_address_id",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "policy",
            "policy_id",
            "vehicle",
            "garaging_address",
            "is_active",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data: dict[str, Any]) -> PolicyVehicle:
        return PolicyVehicle.objects.create(**validated_data)

    def update(self, instance: PolicyVehicle, validated_data: dict[str, Any]) -> PolicyVehicle:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class DriverSerializer(serializers.ModelSerializer):
    client = ClientSummarySerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.filter(is_active=True),
        source="client",
        write_only=True,
    )
    license_class = LookupSerializer(read_only=True)
    license_class_id = serializers.PrimaryKeyRelatedField(
        queryset=LicenseClass.objects.filter(is_active=True),
        source="license_class",
        write_only=True,
    )

    class Meta:
        model = Driver
        fields = (
            "id",
            "client",
            "client_id",
            "first_name",
            "middle_name",
            "last_name",
            "date_of_birth",
            "license_number",
            "license_state",
            "license_class",
            "license_class_id",
            "issue_date",
            "hire_date",
            "violations",
            "accidents",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "client",
            "license_class",
            "is_active",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data: dict[str, Any]) -> Driver:
        return Driver.objects.create(**validated_data)

    def update(self, instance: Driver, validated_data: dict[str, Any]) -> Driver:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PolicyDriverSerializer(serializers.ModelSerializer):
    policy = serializers.UUIDField(source="policy.id", read_only=True)
    policy_id = serializers.PrimaryKeyRelatedField(
        queryset=Policy.objects.filter(is_active=True),
        source="policy",
        write_only=True,
    )
    driver = DriverSerializer(read_only=True)
    driver_id = serializers.PrimaryKeyRelatedField(
        queryset=Driver.objects.filter(is_active=True),
        source="driver",
        write_only=True,
    )

    class Meta:
        model = PolicyDriver
        fields = (
            "id",
            "policy",
            "policy_id",
            "driver",
            "driver_id",
            "status",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "policy",
            "driver",
            "is_active",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data: dict[str, Any]) -> PolicyDriver:
        return PolicyDriver.objects.create(**validated_data)

    def update(self, instance: PolicyDriver, validated_data: dict[str, Any]) -> PolicyDriver:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
