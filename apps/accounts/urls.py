"""URL routes for accounts domain."""
from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EmployeeViewSet

router = DefaultRouter()
router.register("employees", EmployeeViewSet, basename="employee")

app_name = "accounts"

urlpatterns = [
    path("", include(router.urls)),
]

