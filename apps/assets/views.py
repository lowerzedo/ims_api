"""API viewsets for asset management."""
from __future__ import annotations

from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Driver, LossPayee, PolicyDriver, PolicyVehicle, Vehicle
from .serializers import (
    DriverSerializer,
    LossPayeeSerializer,
    PolicyDriverSerializer,
    PolicyVehicleSerializer,
    VehicleSerializer,
)


class BaseSoftDeleteViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset()
        include_inactive = self.request.query_params.get("include_inactive")
        if include_inactive not in {"true", "1", "yes"}:
            queryset = queryset.filter(is_active=True)
        return queryset

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])


class LossPayeeViewSet(BaseSoftDeleteViewSet):
    queryset = LossPayee.objects.select_related("address")
    serializer_class = LossPayeeSerializer
    search_fields = ("name", "contact_person_name")
    ordering_fields = ("name", "created_at")
    ordering = ("name",)


class VehicleViewSet(BaseSoftDeleteViewSet):
    queryset = Vehicle.objects.select_related(
        "client",
        "vehicle_type",
        "loss_payee",
        "loss_payee__address",
    )
    serializer_class = VehicleSerializer
    search_fields = (
        "vin",
        "unit_number",
        "client__company_name",
        "make",
        "model",
    )
    filterset_fields = {
        "client": ["exact"],
        "vehicle_type": ["exact"],
        "loss_payee": ["exact"],
        "year": ["exact", "gte", "lte"],
    }
    ordering_fields = ("vin", "unit_number", "year", "created_at", "updated_at")
    ordering = ("unit_number", "vin")


class PolicyVehicleViewSet(BaseSoftDeleteViewSet):
    queryset = PolicyVehicle.objects.select_related(
        "policy",
        "vehicle",
        "vehicle__client",
        "garaging_address",
    )
    serializer_class = PolicyVehicleSerializer
    filterset_fields = {
        "policy": ["exact"],
        "vehicle": ["exact"],
        "status": ["exact"],
    }
    ordering_fields = ("created_at", "updated_at", "inception_date")
    ordering = ("-created_at",)

    def perform_create(self, serializer: PolicyVehicleSerializer) -> None:
        try:
            serializer.save()
        except IntegrityError as exc:  # pragma: no cover - defensive
            raise serializers.ValidationError("Vehicle is already assigned to this policy.") from exc


class DriverViewSet(BaseSoftDeleteViewSet):
    queryset = Driver.objects.select_related("client", "license_class")
    serializer_class = DriverSerializer
    search_fields = (
        "first_name",
        "last_name",
        "license_number",
        "client__company_name",
    )
    filterset_fields = {
        "client": ["exact"],
        "license_class": ["exact"],
        "license_state": ["exact"],
        "hire_date": ["exact", "gte", "lte"],
    }
    ordering_fields = ("last_name", "first_name", "created_at", "updated_at")
    ordering = ("last_name", "first_name")

    def perform_create(self, serializer: DriverSerializer) -> None:
        try:
            serializer.save()
        except IntegrityError as exc:  # pragma: no cover - defensive
            raise serializers.ValidationError(
                "Driver with this license number already exists for the client."
            ) from exc


class PolicyDriverViewSet(BaseSoftDeleteViewSet):
    queryset = PolicyDriver.objects.select_related(
        "policy",
        "driver",
        "driver__client",
    )
    serializer_class = PolicyDriverSerializer
    filterset_fields = {
        "policy": ["exact"],
        "driver": ["exact"],
        "status": ["exact"],
    }
    ordering_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)

    def perform_create(self, serializer: PolicyDriverSerializer) -> None:
        try:
            serializer.save()
        except IntegrityError as exc:  # pragma: no cover - defensive
            raise serializers.ValidationError("Driver is already assigned to this policy.") from exc
