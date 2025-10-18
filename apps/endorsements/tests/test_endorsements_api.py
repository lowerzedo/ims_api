import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.clients.models import Client
from apps.lookups.models import (
    BusinessType,
    FinanceCompany,
    InsuranceType,
    PolicyStatus,
    PolicyType,
)
from apps.policies.models import CarrierProduct, GeneralAgent, Policy


@pytest.fixture
def api_client(db):
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(email="endorser@example.com", password="password123")


@pytest.fixture
def policy(user):
    client = Client.objects.create(company_name="Atlas Logistics", created_by=user, updated_by=user)
    status = PolicyStatus.objects.filter(is_active=True).first()
    business_type = BusinessType.objects.filter(is_active=True).first()
    insurance_type = InsuranceType.objects.filter(is_active=True).first()
    policy_type = PolicyType.objects.filter(is_active=True).first()
    finance_company = FinanceCompany.objects.filter(is_active=True).first()

    assert all([status, business_type, insurance_type, policy_type, finance_company]), "Expected seeded lookups"

    general_agent = GeneralAgent.objects.create(name="Summit GA", agency_commission="5.00")
    carrier_product = CarrierProduct.objects.create(
        line_of_business="Auto",
        general_agent=general_agent,
        insurance_company_name="Summit Insurance",
        new_business_commission_pct="8.00",
        renewal_commission_pct="7.00",
    )

    return Policy.objects.create(
        client=client,
        policy_number="POL-END-001",
        status=status,
        business_type=business_type,
        insurance_type=insurance_type,
        policy_type=policy_type,
        effective_date="2024-01-01",
        maturity_date="2025-01-01",
        carrier_product=carrier_product,
        finance_company=finance_company,
        created_by=user,
        updated_by=user,
    )


@pytest.mark.django_db
def test_create_endorsement_defaults_name(api_client, user, policy):
    api_client.force_authenticate(user=user)
    url = reverse("endorsements:endorsement-list")
    payload = {
        "policy_id": str(policy.id),
        "effective_date": "2025-02-01",
        "premium_change": "1500.00",
    }

    response = api_client.post(url, payload, format="json")
    assert response.status_code == 201, response.json()
    data = response.json()
    assert data["name"].startswith("Endorsement ")
    assert data["status"] == "draft"
    assert data["current_stage"] == "client"
    assert data["premium_change"] == "1500.00"


@pytest.mark.django_db
def test_record_change_and_list_includes_change_types(api_client, user, policy):
    api_client.force_authenticate(user=user)
    endorsement_url = reverse("endorsements:endorsement-list")
    endorsement_response = api_client.post(
        endorsement_url,
        {"policy_id": str(policy.id)},
        format="json",
    )
    assert endorsement_response.status_code == 201, endorsement_response.json()
    endorsement_id = endorsement_response.json()["id"]

    changes_url = reverse("endorsements:endorsement-change-list")
    change_payload = {
        "endorsement_id": endorsement_id,
        "stage": "vehicles",
        "change_type": "vehicles",
        "summary": "Added 2023 Freightliner",
        "details": {"vin": "3AKJHHDR7LSMS2855"},
    }
    change_response = api_client.post(changes_url, change_payload, format="json")
    assert change_response.status_code == 201

    list_response = api_client.get(endorsement_url, {"policy": str(policy.id)})
    assert list_response.status_code == 200
    result = list_response.json()["results"][0]
    assert result["change_types"] == ["Vehicles"]


@pytest.mark.django_db
def test_complete_endorsement_flow(api_client, user, policy):
    api_client.force_authenticate(user=user)
    endorsement_url = reverse("endorsements:endorsement-list")
    endorsement_response = api_client.post(
        endorsement_url,
        {"policy_id": str(policy.id)},
        format="json",
    )
    assert endorsement_response.status_code == 201, endorsement_response.json()
    endorsement_id = endorsement_response.json()["id"]
    detail_url = reverse("endorsements:endorsement-detail", args=[endorsement_id])

    start_url = reverse("endorsements:endorsement-start", args=[endorsement_id])
    response = api_client.post(start_url, {"stage": "vehicles"}, format="json")
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"
    assert response.json()["current_stage"] == "vehicles"

    advance_url = reverse("endorsements:endorsement-advance", args=[endorsement_id])
    response = api_client.post(advance_url, {"stage": "final"}, format="json")
    assert response.status_code == 200
    assert response.json()["current_stage"] == "final"

    complete_url = reverse("endorsements:endorsement-complete", args=[endorsement_id])
    response = api_client.post(complete_url, format="json")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["completed_at"] is not None

    # Soft delete should retain record but mark inactive
    delete_response = api_client.delete(detail_url)
    assert delete_response.status_code == 204

    list_response = api_client.get(endorsement_url)
    assert list_response.json()["count"] == 0
    list_response = api_client.get(endorsement_url, {"include_inactive": "true"})
    assert list_response.json()["count"] == 1
