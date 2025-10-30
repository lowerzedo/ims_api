"""Client routes."""
from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ClientViewSet

router = DefaultRouter()
router.register("", ClientViewSet, basename="client")

app_name = "clients"

urlpatterns = [
    path("clients/", include(router.urls)),
]
