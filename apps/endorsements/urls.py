"""Routes for endorsements domain."""
from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EndorsementChangeViewSet, EndorsementDocumentViewSet, EndorsementViewSet

router = DefaultRouter()
router.register("endorsements", EndorsementViewSet, basename="endorsement")
router.register("endorsement-changes", EndorsementChangeViewSet, basename="endorsement-change")
router.register("endorsement-documents", EndorsementDocumentViewSet, basename="endorsement-document")

app_name = "endorsements"

urlpatterns = [
    path("", include(router.urls)),
]
