"""Routes for certificate domain."""
from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CertificateHolderViewSet, CertificateViewSet, MasterCertificateViewSet

router = DefaultRouter()
router.register("holders", CertificateHolderViewSet, basename="certificate-holder")
router.register("master-certificates", MasterCertificateViewSet, basename="master-certificate")
router.register("certificates", CertificateViewSet, basename="certificate")

app_name = "certificates"

urlpatterns = [
    path("", include(router.urls)),
]
