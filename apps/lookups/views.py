"""API views for lookup endpoints."""
from __future__ import annotations

from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import (
    AddressType,
    BusinessType,
    ContactType,
    DocumentType,
    FinanceCompany,
    InsuranceType,
    LicenseClass,
    PolicyStatus,
    PolicyType,
    VehicleType,
)
from .serializers import LookupSerializer, PolicyStatusSerializer


class BaseLookupViewSet(ReadOnlyModelViewSet):
    """Shared read-only configuration for lookup viewsets."""

    serializer_class = LookupSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        return self.queryset.filter(is_active=True).order_by("name")


class PolicyStatusViewSet(BaseLookupViewSet):
    queryset = PolicyStatus.objects.all()
    serializer_class = PolicyStatusSerializer


class BusinessTypeViewSet(BaseLookupViewSet):
    queryset = BusinessType.objects.all()


class InsuranceTypeViewSet(BaseLookupViewSet):
    queryset = InsuranceType.objects.all()


class PolicyTypeViewSet(BaseLookupViewSet):
    queryset = PolicyType.objects.all()


class FinanceCompanyViewSet(BaseLookupViewSet):
    queryset = FinanceCompany.objects.all()


class ContactTypeViewSet(BaseLookupViewSet):
    queryset = ContactType.objects.all()


class AddressTypeViewSet(BaseLookupViewSet):
    queryset = AddressType.objects.all()


class VehicleTypeViewSet(BaseLookupViewSet):
    queryset = VehicleType.objects.all()


class LicenseClassViewSet(BaseLookupViewSet):
    queryset = LicenseClass.objects.all()


class DocumentTypeViewSet(BaseLookupViewSet):
    queryset = DocumentType.objects.all()
