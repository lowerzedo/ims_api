"""URL Configuration for the IMS API."""
from __future__ import annotations

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.common.views import health_check

admin.site.site_header = "Insurance Management System Admin"
admin.site.site_title = "IMS Admin"
admin.site.index_title = "Administration"

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/health/", health_check, name="health-check"),
    path("api/v1/lookups/", include("apps.lookups.urls", namespace="lookups")),
    path("api/v1/policies/", include("apps.policies.urls", namespace="policies")),
    path("api/v1/assets/", include("apps.assets.urls", namespace="assets")),
    path("api/v1/endorsements/", include("apps.endorsements.urls", namespace="endorsements")),
    path("api/v1/certificates/", include("apps.certificates.urls", namespace="certificates")),
    path("api/v1/accounts/", include("apps.accounts.urls", namespace="accounts")),
    path("api/v1/", include("apps.common.urls", namespace="common")),
    path("api/v1/", include("apps.clients.urls", namespace="clients")),
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/docs/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("api/auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
