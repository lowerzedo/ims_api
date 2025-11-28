"""Client routes."""
from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AddressViewSet, ClientViewSet

client_router = DefaultRouter()
client_router.register("", ClientViewSet, basename="client")

address_router = DefaultRouter()
address_router.register("", AddressViewSet, basename="address")

app_name = "clients"

urlpatterns = [
    path("clients/", include(client_router.urls)),
    path("addresses/", include(address_router.urls)),
]
