"""Serializers for client domain."""
from __future__ import annotations

from typing import Any

from django.db import transaction
from rest_framework import serializers

from apps.lookups.models import AddressType, ContactType
from apps.lookups.serializers import LookupSerializer

from .models import Address, Client, ClientAddress, ClientDBA, Contact


class ClientDBASerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientDBA
        fields = ("id", "dba_name", "is_active")
        read_only_fields = ("id", "is_active")


class ContactSerializer(serializers.ModelSerializer):
    contact_type = LookupSerializer(read_only=True)
    contact_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ContactType.objects.filter(is_active=True),
        source="contact_type",
        write_only=True,
    )

    class Meta:
        model = Contact
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "nickname",
            "contact_type",
            "contact_type_id",
            "is_active",
        )
        read_only_fields = ("id", "contact_type", "is_active")


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("id", "street_address", "city", "state", "zip_code")
        read_only_fields = ("id",)


class ClientAddressSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    address_type = LookupSerializer(read_only=True)
    address_type_id = serializers.PrimaryKeyRelatedField(
        queryset=AddressType.objects.filter(is_active=True),
        source="address_type",
        write_only=True,
    )

    class Meta:
        model = ClientAddress
        fields = (
            "id",
            "address",
            "address_type",
            "address_type_id",
            "rating",
            "is_active",
        )
        read_only_fields = ("id", "address_type", "is_active")


class ClientSerializer(serializers.ModelSerializer):
    dbas = ClientDBASerializer(many=True, required=False)
    contacts = ContactSerializer(many=True, required=False)
    addresses = ClientAddressSerializer(many=True, required=False)

    class Meta:
        model = Client
        fields = (
            "id",
            "company_name",
            "dot_number",
            "fein",
            "date_of_authority",
            "referral_source",
            "factoring_company",
            "dbas",
            "contacts",
            "addresses",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "is_active", "created_at", "updated_at")

    def _replace_related(self, client: Client, field: str, items: list[dict[str, Any]]) -> None:
        manager = getattr(client, field)
        manager.all().delete()
        if field == "dbas":
            for item in items:
                manager.create(dba_name=item["dba_name"])
        elif field == "contacts":
            for item in items:
                contact_type = item.pop("contact_type")
                manager.create(contact_type=contact_type, **item)
        elif field == "addresses":
            for item in items:
                address_data = item.pop("address")
                address = Address.objects.create(**address_data)
                manager.create(address=address, **item)

    def create(self, validated_data: dict[str, Any]) -> Client:
        dbas_data = validated_data.pop("dbas", [])
        contacts_data = validated_data.pop("contacts", [])
        addresses_data = validated_data.pop("addresses", [])

        with transaction.atomic():
            client = Client.objects.create(**validated_data)
            self._replace_related(client, "dbas", dbas_data)
            self._replace_related(client, "contacts", contacts_data)
            self._replace_related(client, "addresses", addresses_data)
        return client

    def update(self, instance: Client, validated_data: dict[str, Any]) -> Client:
        dbas_data = validated_data.pop("dbas", None)
        contacts_data = validated_data.pop("contacts", None)
        addresses_data = validated_data.pop("addresses", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        with transaction.atomic():
            instance.save()
            if dbas_data is not None:
                self._replace_related(instance, "dbas", dbas_data)
            if contacts_data is not None:
                self._replace_related(instance, "contacts", contacts_data)
            if addresses_data is not None:
                self._replace_related(instance, "addresses", addresses_data)
        return instance

    def to_internal_value(self, data: Any) -> Any:
        value = super().to_internal_value(data)

        def merge_raw_items(raw_items, cleaned_items):
            merged: list[dict[str, Any]] = []
            for raw, cleaned in zip(raw_items, cleaned_items):
                merged_item = dict(cleaned)
                for key, val in raw.items():
                    if key.endswith('_id'):
                        continue
                    if key not in merged_item:
                        merged_item[key] = val
                merged.append(merged_item)
            return merged

        for key in ("dbas", "contacts", "addresses"):
            if key in data and value.get(key):
                value[key] = merge_raw_items(data.get(key) or [], value[key])
        return value
