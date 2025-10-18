"""URL configuration for asset endpoints."""
from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LossPayeeViewSet, PolicyVehicleViewSet, VehicleViewSet

router = DefaultRouter()
router.register("loss-payees", LossPayeeViewSet, basename="loss-payee")
router.register("vehicles", VehicleViewSet, basename="vehicle")
router.register("policy-vehicles", PolicyVehicleViewSet, basename="policy-vehicle")

app_name = "assets"

urlpatterns = [
    path("", include(router.urls)),
]
