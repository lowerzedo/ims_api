"""Serializers for common domain."""
from __future__ import annotations

from rest_framework import serializers

from apps.accounts.models import User

from .models import ActivityLog


class UserSummarySerializer(serializers.ModelSerializer):
    """Lightweight user representation for activity logs."""

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "full_name")
        read_only_fields = fields

    def get_full_name(self, obj: User) -> str:
        return obj.full_name


class ActivityLogSerializer(serializers.ModelSerializer):
    """Serializer for activity log entries (Timeline)."""

    action_type_display = serializers.CharField(
        source="get_action_type_display", read_only=True
    )
    performed_by = UserSummarySerializer(read_only=True)
    carrier_name = serializers.CharField(read_only=True)
    policy_number = serializers.CharField(read_only=True)

    # Related entity summaries
    client_name = serializers.SerializerMethodField()
    vehicle_info = serializers.SerializerMethodField()
    driver_info = serializers.SerializerMethodField()
    endorsement_name = serializers.SerializerMethodField()

    class Meta:
        model = ActivityLog
        fields = (
            "id",
            "action_type",
            "action_type_display",
            "transaction_name",
            "description",
            "notes",
            "timestamp",
            # Related IDs
            "client",
            "policy",
            "endorsement",
            "vehicle",
            "driver",
            # Computed fields
            "client_name",
            "carrier_name",
            "policy_number",
            "vehicle_info",
            "driver_info",
            "endorsement_name",
            # User
            "performed_by",
            "metadata",
        )
        read_only_fields = fields

    def get_client_name(self, obj: ActivityLog) -> str | None:
        if obj.client:
            return obj.client.company_name
        return None

    def get_vehicle_info(self, obj: ActivityLog) -> dict | None:
        if obj.vehicle:
            return {
                "id": str(obj.vehicle.id),
                "vin": obj.vehicle.vin,
                "unit_number": obj.vehicle.unit_number,
                "year": obj.vehicle.year,
                "make": obj.vehicle.make,
                "model": obj.vehicle.model,
            }
        return None

    def get_driver_info(self, obj: ActivityLog) -> dict | None:
        if obj.driver:
            return {
                "id": str(obj.driver.id),
                "first_name": obj.driver.first_name,
                "last_name": obj.driver.last_name,
                "license_number": obj.driver.license_number,
            }
        return None

    def get_endorsement_name(self, obj: ActivityLog) -> str | None:
        if obj.endorsement:
            return obj.endorsement.name
        return None


class ActivityLogCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating activity log entries."""

    class Meta:
        model = ActivityLog
        fields = (
            "action_type",
            "transaction_name",
            "description",
            "notes",
            "client",
            "policy",
            "endorsement",
            "vehicle",
            "driver",
            "metadata",
        )

    def create(self, validated_data):
        # Auto-set performed_by from request user
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["performed_by"] = request.user
        return super().create(validated_data)

