import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.assets.models import Driver, Vehicle
from apps.certificates.models import Certificate
from apps.clients.models import Client
from apps.lookups.models import (
    BusinessType,
    FinanceCompany,
    InsuranceType,
    LicenseClass,
    PolicyStatus,
    PolicyType,
    VehicleType,
)
from apps.policies.models import CarrierProduct, GeneralAgent, Policy


@pytest.fixture
def api_client(db):
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(email="issuer@example.com", password="password123")


@pytest.fixture(autouse=True)
def media_storage(settings, tmp_path):
    settings.MEDIA_ROOT = tmp_path / "media"
    return settings.MEDIA_ROOT


@pytest.fixture
def lookup_values(db):
    status = PolicyStatus.objects.filter(is_active=True).first()
    business_type = BusinessType.objects.filter(is_active=True).first()
    insurance_type = InsuranceType.objects.filter(is_active=True).first()
    policy_type = PolicyType.objects.filter(is_active=True).first()
    finance_company = FinanceCompany.objects.filter(is_active=True).first()
    assert status and business_type and insurance_type and policy_type and finance_company
    return {
        "status": status,
        "business_type": business_type,
        "insurance_type": insurance_type,
        "policy_type": policy_type,
        "finance_company": finance_company,
    }


@pytest.fixture
def vehicle_type(db):
    obj = VehicleType.objects.filter(is_active=True).first()
    assert obj is not None, "Expected seeded vehicle type"
    return obj


@pytest.fixture
def license_class(db):
    obj = LicenseClass.objects.filter(is_active=True).first()
    assert obj is not None, "Expected seeded license class"
    return obj


@pytest.fixture
def client(user):
    return Client.objects.create(company_name="Blue Line Logistics", created_by=user, updated_by=user)


@pytest.fixture
def policy(user, client, lookup_values):
    general_agent = GeneralAgent.objects.create(name="Everest GA", agency_commission="5.00")
    carrier_product = CarrierProduct.objects.create(
        line_of_business="Auto",
        general_agent=general_agent,
        insurance_company_name="Everest Insurance",
        new_business_commission_pct="8.00",
        renewal_commission_pct="7.00",
    )

    return Policy.objects.create(
        client=client,
        policy_number="POL-CERT-001",
        status=lookup_values["status"],
        business_type=lookup_values["business_type"],
        insurance_type=lookup_values["insurance_type"],
        policy_type=lookup_values["policy_type"],
        effective_date="2024-01-01",
        maturity_date="2025-01-01",
        carrier_product=carrier_product,
        finance_company=lookup_values["finance_company"],
        created_by=user,
        updated_by=user,
    )


@pytest.mark.django_db
def test_create_certificate_holder(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse("certificates:certificate-holder-list")
    payload = {
        "name": "Acme Warehouse Holdings",
        "contact_person": "Jane Smith",
        "email": "jane@example.com",
        "address": {
            "street_address": "500 Market St",
            "city": "Austin",
            "state": "TX",
            "zip_code": "78701",
        },
    }

    response = api_client.post(url, payload, format="json")
    assert response.status_code == 201, response.json()
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["address"]["city"] == "Austin"


@pytest.mark.django_db
def test_issue_certificate_generates_pdf(
    api_client,
    user,
    policy,
    client,
    vehicle_type,
    license_class,
):
    api_client.force_authenticate(user=user)

    master_url = reverse("certificates:master-certificate-list")
    master_payload = {
        "policy_id": str(policy.id),
        "name": "Primary Certificate",
        "settings": {"coverages": ["Auto Liability"], "show_values": True},
    }
    master_response = api_client.post(master_url, master_payload, format="json")
    assert master_response.status_code == 201, master_response.json()
    master_id = master_response.json()["id"]

    holder_url = reverse("certificates:certificate-holder-list")
    holder_payload = {
        "name": "Logistics Hub LLC",
        "contact_person": "Sam Broker",
        "phone_number": "555-1212",
        "address": {
            "street_address": "100 Depot Rd",
            "city": "Dallas",
            "state": "TX",
            "zip_code": "75201",
        },
    }
    holder_response = api_client.post(holder_url, holder_payload, format="json")
    assert holder_response.status_code == 201, holder_response.json()
    holder_id = holder_response.json()["id"]

    vehicle = Vehicle.objects.create(
        client=client,
        vin="1XPWD40X1ED999999",
        unit_number="UNIT-99",
        vehicle_type=vehicle_type,
        year=2024,
        make="Peterbilt",
        model="579",
        pd_amount="120000.00",
    )
    driver = Driver.objects.create(
        client=client,
        first_name="Alex",
        last_name="Johnson",
        date_of_birth="1990-05-01",
        license_number="TX1234567",
        license_state="TX",
        license_class=license_class,
    )

    certificate_url = reverse("certificates:certificate-list")
    certificate_payload = {
        "master_certificate_id": master_id,
        "certificate_holder_id": holder_id,
        "vehicle_ids": [str(vehicle.id)],
        "driver_ids": [str(driver.id)],
    }
    certificate_response = api_client.post(certificate_url, certificate_payload, format="json")
    assert certificate_response.status_code == 201, certificate_response.json()
    data = certificate_response.json()
    assert len(data["vehicles"]) == 1
    assert len(data["drivers"]) == 1
    assert data["verification_code"]

    certificate = Certificate.objects.get(id=data["id"])
    assert certificate.document.name.endswith(".pdf")
    stored_path = certificate.document.path
    with open(stored_path, "rb") as fp:
        content = fp.read()
    assert content.startswith(b"%PDF"), "Expected generated PDF document"
