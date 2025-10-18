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
from .serializers import (
    AddressTypeSerializer,
    BusinessTypeSerializer,
    ContactTypeSerializer,
    DocumentTypeSerializer,
    FinanceCompanySerializer,
    InsuranceTypeSerializer,
    LicenseClassSerializer,
    PolicyStatusSerializer,
    PolicyTypeSerializer,
    VehicleTypeSerializer,
)


class BaseLookupViewSet(ReadOnlyModelViewSet):
    """Shared read-only configuration for lookup viewsets."""

    permission_classes = (AllowAny,)

    def get_queryset(self):
        return self.queryset.filter(is_active=True).order_by("name")


class PolicyStatusViewSet(BaseLookupViewSet):
    queryset = PolicyStatus.objects.all()
    serializer_class = PolicyStatusSerializer


class BusinessTypeViewSet(BaseLookupViewSet):
    queryset = BusinessType.objects.all()
    serializer_class = BusinessTypeSerializer


class InsuranceTypeViewSet(BaseLookupViewSet):
    queryset = InsuranceType.objects.all()
    serializer_class = InsuranceTypeSerializer


class PolicyTypeViewSet(BaseLookupViewSet):
    queryset = PolicyType.objects.all()
    serializer_class = PolicyTypeSerializer


class FinanceCompanyViewSet(BaseLookupViewSet):
    queryset = FinanceCompany.objects.all()
    serializer_class = FinanceCompanySerializer


class ContactTypeViewSet(BaseLookupViewSet):
    queryset = ContactType.objects.all()
    serializer_class = ContactTypeSerializer


class AddressTypeViewSet(BaseLookupViewSet):
    queryset = AddressType.objects.all()
    serializer_class = AddressTypeSerializer


class VehicleTypeViewSet(BaseLookupViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer


class LicenseClassViewSet(BaseLookupViewSet):
    queryset = LicenseClass.objects.all()
    serializer_class = LicenseClassSerializer


class DocumentTypeViewSet(BaseLookupViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer
