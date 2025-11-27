"""Serializers for the accounts domain."""
from __future__ import annotations

from rest_framework import serializers

from .models import User


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for employee users with commission information."""

    full_name = serializers.SerializerMethodField()

    def get_full_name(self, obj: User) -> str:
        return obj.full_name

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "phone_number",
            "role",
            "commission_rate",
            "is_active",
            "date_joined",
        )
        read_only_fields = fields

