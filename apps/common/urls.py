"""URL routes for common domain."""
from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ActivityLogViewSet

router = DefaultRouter()
router.register("activity-logs", ActivityLogViewSet, basename="activity-log")

app_name = "common"

urlpatterns = [
    path("", include(router.urls)),
]

