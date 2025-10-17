"""Serializers for lookup tables."""
from __future__ import annotations

from rest_framework import serializers


class LookupSerializer(serializers.ModelSerializer):
    """Base serializer exposing the common lookup fields."""

    class Meta:
        fields = ("id", "name", "is_active")
        read_only_fields = fields


class PolicyStatusSerializer(LookupSerializer):
    class Meta(LookupSerializer.Meta):
        fields = LookupSerializer.Meta.fields + ("description",)
        read_only_fields = fields
