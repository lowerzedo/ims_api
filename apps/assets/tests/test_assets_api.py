import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.clients.models import Address, Client
from apps.lookups.models import LicenseClass, VehicleType
from apps.policies.models import CarrierProduct, GeneralAgent, Policy
from apps.lookups.models import (
    BusinessType,
    InsuranceType,
    PolicyStatus,
    PolicyType,
    FinanceCompany,
)


@pytest.fixture
def api_client(db):
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(email="user@example.com", password="password123")


@pytest.fixture
def client(user):
    return Client.objects.create(company_name="Road Runner", created_by=user, updated_by=user)


@pytest.fixture
def license_class(db):
    license_class = LicenseClass.objects.filter(is_active=True).first()
    assert license_class is not None, "Expected seeded license classes"
    return license_class


@pytest.fixture
def vehicle_type(db):
    vehicle_type = VehicleType.objects.filter(is_active=True).first()
    assert vehicle_type is not None, "Expected seeded vehicle types"
    return vehicle_type


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
def carrier_product(db):
    ga = GeneralAgent.objects.create(name="Sample GA", agency_commission="5.00")
    return CarrierProduct.objects.create(
        line_of_business="Auto",
        general_agent=ga,
        insurance_company_name="Acme Insurance",
        new_business_commission_pct="8.00",
        renewal_commission_pct="7.00",
    )


@pytest.fixture
def policy(user, client, carrier_product, lookup_values):
    return Policy.objects.create(
        client=client,
        policy_number="POL-VEH-1",
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
def test_create_loss_payee(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse("assets:loss-payee-list")
    payload = {
        "name": "Bank of Example",
        "email": "loss@example.com",
        "preference": "EMAIL",
        "address": {
            "street_address": "100 Main St",
            "city": "Austin",
            "state": "TX",
            "zip_code": "78701",
        },
    }
    response = api_client.post(url, payload, format="json")
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Bank of Example"
    assert data["address"]["city"] == "Austin"


@pytest.mark.django_db
def test_create_vehicle_with_loss_payee(api_client, user, client, vehicle_type):
    api_client.force_authenticate(user=user)
    loss_payee_url = reverse("assets:loss-payee-list")
    loss_response = api_client.post(
        loss_payee_url,
        {
            "name": "Bank of Example",
            "address": {
                "street_address": "100 Main St",
                "city": "Austin",
                "state": "TX",
                "zip_code": "78701",
            },
        },
        format="json",
    )
    assert loss_response.status_code == 201
    loss_payee_id = loss_response.json()["id"]

    vehicle_url = reverse("assets:vehicle-list")
    payload = {
        "client_id": str(client.id),
        "vin": "1XPWD40X1ED215307",
        "unit_number": "UNIT-001",
        "vehicle_type_id": str(vehicle_type.id),
        "year": 2024,
        "make": "Peterbilt",
        "model": "579",
        "gvw": 80000,
        "pd_amount": "120000.00",
        "deductible": "1000.00",
        "loss_payee_id": loss_payee_id,
    }
    response = api_client.post(vehicle_url, payload, format="json")
    assert response.status_code == 201
    data = response.json()
    assert data["vin"] == payload["vin"]
    assert data["loss_payee"]["id"] == loss_payee_id


@pytest.mark.django_db
def test_soft_delete_vehicle(api_client, user, client, vehicle_type):
    api_client.force_authenticate(user=user)
    vehicle = client.vehicles.create(
        vin="1FTSW21R08EC46906",
        vehicle_type=vehicle_type,
        year=2023,
        make="Ford",
        model="F-750",
    )

    url = reverse("assets:vehicle-detail", args=[vehicle.id])
    response = api_client.delete(url)
    assert response.status_code == 204
    vehicle.refresh_from_db()
    assert vehicle.is_active is False


@pytest.mark.django_db
def test_assign_vehicle_to_policy(api_client, user, client, vehicle_type, policy):
    api_client.force_authenticate(user=user)
    address = Address.objects.create(
        street_address="200 Depot Rd",
        city="Dallas",
        state="TX",
        zip_code="75201",
    )
    vehicle = client.vehicles.create(
        vin="3AKJGLDR5FSFK1234",
        vehicle_type=vehicle_type,
        year=2022,
        make="Freightliner",
        model="Cascadia",
    )

    url = reverse("assets:policy-vehicle-list")
    payload = {
        "policy_id": str(policy.id),
        "vehicle_id": str(vehicle.id),
        "status": "active",
        "garaging_address_id": str(address.id),
        "inception_date": "2024-02-01",
    }
    response = api_client.post(url, payload, format="json")
    assert response.status_code == 201
    data = response.json()
    assert data["vehicle"]["vin"] == vehicle.vin
    assert data["garaging_address"]["city"] == "Dallas"

    # Ensure unique constraint prevents duplicates
    dup_response = api_client.post(url, payload, format="json")
    assert dup_response.status_code == 400


@pytest.mark.django_db
def test_create_driver(api_client, user, client, license_class):
    api_client.force_authenticate(user=user)
    url = reverse("assets:driver-list")
    payload = {
        "client_id": str(client.id),
        "first_name": "Jane",
        "middle_name": "Q",
        "last_name": "Doe",
        "date_of_birth": "1990-03-15",
        "license_number": "TX1234567",
        "license_state": "TX",
        "license_class_id": str(license_class.id),
        "issue_date": "2020-01-01",
        "hire_date": "2023-05-01",
        "violations": 1,
        "accidents": 0,
    }
    response = api_client.post(url, payload, format="json")
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "Jane"
    assert data["license_class"]["id"] == str(license_class.id)


@pytest.mark.django_db
def test_assign_driver_to_policy(api_client, user, client, license_class, policy):
    api_client.force_authenticate(user=user)
    driver_url = reverse("assets:driver-list")
    driver_payload = {
        "client_id": str(client.id),
        "first_name": "John",
        "last_name": "Smith",
        "date_of_birth": "1985-07-04",
        "license_number": "CA7654321",
        "license_state": "CA",
        "license_class_id": str(license_class.id),
    }
    driver_response = api_client.post(driver_url, driver_payload, format="json")
    assert driver_response.status_code == 201
    driver_id = driver_response.json()["id"]

    policy_driver_url = reverse("assets:policy-driver-list")
    payload = {
        "policy_id": str(policy.id),
        "driver_id": driver_id,
        "status": "active",
    }
    response = api_client.post(policy_driver_url, payload, format="json")
    assert response.status_code == 201
    data = response.json()
    assert data["driver"]["id"] == driver_id

    dup_response = api_client.post(policy_driver_url, payload, format="json")
    assert dup_response.status_code == 400
