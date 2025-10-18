"""Serializers for endorsement workflow."""
from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any

from django.utils import timezone
from rest_framework import serializers

from apps.accounts.models import User
from apps.policies.models import Policy

from .models import Endorsement, EndorsementChange


class UserSummarySerializer(serializers.ModelSerializer):
    """Lightweight representation of a user."""

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "role")
        read_only_fields = fields


class EndorsementChangeSerializer(serializers.ModelSerializer):
    endorsement = serializers.UUIDField(source="endorsement.id", read_only=True)
    endorsement_id = serializers.PrimaryKeyRelatedField(
        queryset=Endorsement.objects.filter(is_active=True),
        source="endorsement",
        write_only=True,
    )
    created_by = UserSummarySerializer(read_only=True)
    created_by_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True),
        source="created_by",
        write_only=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = EndorsementChange
        fields = (
            "id",
            "endorsement",
            "endorsement_id",
            "stage",
            "change_type",
            "summary",
            "details",
            "created_by",
            "created_by_id",
            "created_at",
            "updated_at",
            "is_active",
        )
        read_only_fields = ("id", "endorsement", "created_by", "created_at", "updated_at", "is_active")


class EndorsementSerializer(serializers.ModelSerializer):
    policy = serializers.UUIDField(source="policy.id", read_only=True)
    policy_id = serializers.PrimaryKeyRelatedField(
        queryset=Policy.objects.filter(is_active=True),
        source="policy",
        write_only=True,
    )
    name = serializers.CharField(required=False)
    created_by = UserSummarySerializer(read_only=True)
    updated_by = UserSummarySerializer(read_only=True)
    created_by_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True),
        source="created_by",
        write_only=True,
        allow_null=True,
        required=False,
    )
    updated_by_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True),
        source="updated_by",
        write_only=True,
        allow_null=True,
        required=False,
    )
    change_types = serializers.SerializerMethodField()
    changes = EndorsementChangeSerializer(many=True, read_only=True)

    class Meta:
        model = Endorsement
        fields = (
            "id",
            "policy",
            "policy_id",
            "name",
            "status",
            "current_stage",
            "effective_date",
            "premium_change",
            "fees_change",
            "taxes_change",
            "agency_fee_change",
            "total_premium_change",
            "notes",
            "completed_at",
            "created_by",
            "updated_by",
            "created_by_id",
            "updated_by_id",
            "change_types",
            "changes",
            "created_at",
            "updated_at",
            "is_active",
        )
        read_only_fields = (
            "id",
            "policy",
            "status",
            "completed_at",
            "created_by",
            "updated_by",
            "change_types",
            "changes",
            "created_at",
            "updated_at",
            "is_active",
        )

    def get_change_types(self, obj: Endorsement) -> list[str]:
        ordering = {choice[0]: idx for idx, choice in enumerate(EndorsementChange.ChangeType.choices)}
        labels = {}
        for change in obj.changes.all():
            key = change.change_type
            if key not in labels:
                labels[key] = change.get_change_type_display()
        return [labels[key] for key in sorted(labels, key=lambda item: ordering.get(item, 999))]

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        for field in (
            "premium_change",
            "fees_change",
            "taxes_change",
            "agency_fee_change",
            "total_premium_change",
        ):
            value = attrs.get(field)
            if value is None:
                continue
            attrs[field] = Decimal(value)
        return attrs

    def _generate_name(self, *, effective_on: date | None) -> str:
        base_date = effective_on or timezone.now().date()
        return f"Endorsement {base_date.strftime('%m/%d/%Y')}"

    def create(self, validated_data: dict[str, Any]) -> Endorsement:
        name = validated_data.get("name")
        effective = validated_data.get("effective_date")
        if not name:
            validated_data["name"] = self._generate_name(effective_on=effective)
        endorsement = Endorsement.objects.create(**validated_data)
        return endorsement

    def update(self, instance: Endorsement, validated_data: dict[str, Any]) -> Endorsement:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
