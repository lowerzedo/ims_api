"""URL configuration for lookup endpoints."""
from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AddressTypeViewSet,
    BusinessTypeViewSet,
    ContactTypeViewSet,
    DocumentTypeViewSet,
    FinanceCompanyViewSet,
    InsuranceTypeViewSet,
    LicenseClassViewSet,
    PolicyStatusViewSet,
    PolicyTypeViewSet,
    VehicleTypeViewSet,
)

router = DefaultRouter()
router.register("policy-statuses", PolicyStatusViewSet, basename="lookup-policy-status")
router.register("business-types", BusinessTypeViewSet, basename="lookup-business-type")
router.register("insurance-types", InsuranceTypeViewSet, basename="lookup-insurance-type")
router.register("policy-types", PolicyTypeViewSet, basename="lookup-policy-type")
router.register("finance-companies", FinanceCompanyViewSet, basename="lookup-finance-company")
router.register("contact-types", ContactTypeViewSet, basename="lookup-contact-type")
router.register("address-types", AddressTypeViewSet, basename="lookup-address-type")
router.register("vehicle-types", VehicleTypeViewSet, basename="lookup-vehicle-type")
router.register("license-classes", LicenseClassViewSet, basename="lookup-license-class")
router.register("document-types", DocumentTypeViewSet, basename="lookup-document-type")


app_name = "lookups"

urlpatterns = [
    path("", include(router.urls)),
]
