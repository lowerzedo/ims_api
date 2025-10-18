"""URL routes for the policies domain."""
from __future__ import annotations

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CarrierProductViewSet,
    GeneralAgentViewSet,
    PolicyViewSet,
    ReferralCompanyViewSet,
)

router = DefaultRouter()
router.register("policies", PolicyViewSet, basename="policy")
router.register("general-agents", GeneralAgentViewSet, basename="general-agent")
router.register("carrier-products", CarrierProductViewSet, basename="carrier-product")
router.register("referral-companies", ReferralCompanyViewSet, basename="referral-company")

app_name = "policies"

urlpatterns = [
    path("", include(router.urls)),
]
