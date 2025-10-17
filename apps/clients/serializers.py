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

    def _sync_dbas(self, client: Client, items: list[dict[str, Any]], *, clear_existing: bool) -> None:
        manager = client.dbas
        existing = {str(obj.id): obj for obj in manager.all()}

        if clear_existing:
            manager.all().delete()
            existing = {}

        for raw in items:
            data = dict(raw)
            obj_id = str(data.pop("id", "") or "")
            is_active = data.pop("is_active", True)
            dba_name = data.get("dba_name")

            if obj_id and obj_id in existing and not clear_existing:
                obj = existing[obj_id]
                if dba_name is not None:
                    obj.dba_name = dba_name
                obj.is_active = is_active
                obj.save(update_fields=["dba_name", "is_active", "updated_at"])
                continue

            if not dba_name:
                raise serializers.ValidationError("dba_name is required for client DBAs.")
            manager.create(dba_name=dba_name, is_active=is_active)

    def _sync_contacts(self, client: Client, items: list[dict[str, Any]], *, clear_existing: bool) -> None:
        manager = client.contacts
        existing = {str(obj.id): obj for obj in manager.all()}

        if clear_existing:
            manager.all().delete()
            existing = {}

        for raw in items:
            data = dict(raw)
            obj_id = str(data.pop("id", "") or "")
            is_active = data.pop("is_active", True)
            contact_type = data.pop("contact_type", None)

            if obj_id and obj_id in existing and not clear_existing:
                obj = existing[obj_id]
                for field in ["first_name", "last_name", "email", "phone_number", "nickname"]:
                    if field in data:
                        setattr(obj, field, data[field])
                if contact_type is not None:
                    obj.contact_type = contact_type
                obj.is_active = is_active
                obj.save(update_fields=[
                    "first_name",
                    "last_name",
                    "email",
                    "phone_number",
                    "nickname",
                    "contact_type",
                    "is_active",
                    "updated_at",
                ])
                continue

            if contact_type is None:
                raise serializers.ValidationError("contact_type_id is required for contacts.")
            manager.create(contact_type=contact_type, is_active=is_active, **data)

    def _delete_address_link(self, link: ClientAddress) -> None:
        address = link.address
        link.delete()
        if not address.client_links.exists():
            address.delete()

    def _sync_addresses(self, client: Client, items: list[dict[str, Any]], *, clear_existing: bool) -> None:
        links = client.addresses.select_related("address")
        existing = {str(link.id): link for link in links}

        if clear_existing:
            for link in links:
                self._delete_address_link(link)
            existing = {}

        for raw in items:
            data = dict(raw)
            link_id = str(data.pop("id", "") or "")
            is_active = data.pop("is_active", True)
            address_type = data.pop("address_type", None)
            address_payload = data.pop("address", None)

            if link_id and link_id in existing and not clear_existing:
                link = existing[link_id]
                if address_payload:
                    address = link.address
                    for field in ["street_address", "city", "state", "zip_code"]:
                        if field in address_payload:
                            setattr(address, field, address_payload[field])
                    address.save(update_fields=["street_address", "city", "state", "zip_code", "updated_at"])
                if address_type is not None:
                    link.address_type = address_type
                if "rating" in data:
                    link.rating = data["rating"]
                link.is_active = is_active
                link.save(update_fields=["address_type", "rating", "is_active", "updated_at"])
                continue

            if not address_payload or address_type is None:
                raise serializers.ValidationError(
                    "address and address_type_id are required when creating a client address."
                )
            address = Address.objects.create(**address_payload)
            client.addresses.create(
                address=address,
                address_type=address_type,
                rating=data.get("rating"),
                is_active=is_active,
            )

    def create(self, validated_data: dict[str, Any]) -> Client:
        dbas_data = validated_data.pop("dbas", [])
        contacts_data = validated_data.pop("contacts", [])
        addresses_data = validated_data.pop("addresses", [])

        with transaction.atomic():
            client = Client.objects.create(**validated_data)
            self._sync_dbas(client, dbas_data, clear_existing=True)
            self._sync_contacts(client, contacts_data, clear_existing=True)
            self._sync_addresses(client, addresses_data, clear_existing=True)
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
                clear = not self.partial or not dbas_data
                self._sync_dbas(instance, dbas_data, clear_existing=clear)
            if contacts_data is not None:
                clear = not self.partial or not contacts_data
                self._sync_contacts(instance, contacts_data, clear_existing=clear)
            if addresses_data is not None:
                clear = not self.partial or not addresses_data
                self._sync_addresses(instance, addresses_data, clear_existing=clear)
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
