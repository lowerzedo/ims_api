from decimal import Decimal

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
from apps.policies.models import CarrierProduct, Coverage, GeneralAgent, Policy, ReferralCompany


@pytest.fixture
def api_client(db):
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(email="user@example.com", password="password123")


@pytest.fixture
def producer(db):
    return User.objects.create_user(email="producer@example.com", password="password123")


@pytest.fixture
def account_manager(db):
    return User.objects.create_user(email="manager@example.com", password="password123")


@pytest.fixture
def client(user):
    return Client.objects.create(company_name="Acme Logistics", created_by=user, updated_by=user)


@pytest.fixture
def general_agent(db):
    return GeneralAgent.objects.create(name="Progressive GA", agency_commission="5.00")


@pytest.fixture
def carrier_product(general_agent):
    return CarrierProduct.objects.create(
        line_of_business="Auto Liability",
        general_agent=general_agent,
        insurance_company_name="Progressive",
        new_business_commission_pct="8.50",
        renewal_commission_pct="7.00",
    )


@pytest.fixture
def referral_company(db):
    return ReferralCompany.objects.create(name="Boston Referral", rate="2.50")


@pytest.fixture
def lookup_values(db):
    status = PolicyStatus.objects.filter(is_active=True).first()
    business_type = BusinessType.objects.filter(is_active=True).first()
    insurance_type = InsuranceType.objects.filter(is_active=True).first()
    policy_type = PolicyType.objects.filter(is_active=True).first()
    finance_company = FinanceCompany.objects.filter(is_active=True).first()

    assert status is not None, "Expected seeded policy statuses"
    assert business_type is not None, "Expected seeded business types"
    assert insurance_type is not None, "Expected seeded insurance types"
    assert policy_type is not None, "Expected seeded policy types"
    assert finance_company is not None, "Expected seeded finance companies"

    return {
        "status": status,
        "business_type": business_type,
        "insurance_type": insurance_type,
        "policy_type": policy_type,
        "finance_company": finance_company,
    }


@pytest.mark.django_db
def test_create_policy_with_nested_financials_and_coverages(
    api_client,
    user,
    producer,
    account_manager,
    client,
    carrier_product,
    referral_company,
    lookup_values,
):
    api_client.force_authenticate(user=user)
    url = reverse("policies:policy-list")
    payload = {
        "client_id": str(client.id),
        "policy_number": "POL-123",
        "status_id": str(lookup_values["status"].id),
        "business_type_id": str(lookup_values["business_type"].id),
        "insurance_type_id": str(lookup_values["insurance_type"].id),
        "policy_type_id": str(lookup_values["policy_type"].id),
        "effective_date": "2024-01-01",
        "maturity_date": "2025-01-01",
        "carrier_product_id": str(carrier_product.id),
        "finance_company_id": str(lookup_values["finance_company"].id),
        "producer_id": str(producer.id),
        "account_manager_id": str(account_manager.id),
        "account_manager_rate": "9.50",
        "referral_company_id": str(referral_company.id),
        "financials": {
            "original_pure_premium": "10000.00",
            "latest_pure_premium": "10500.00",
            "broker_fee": "250.00",
            "taxes": "120.00",
            "agency_fee": "300.00",
            "total_premium": "11000.00",
            "down_payment": "2000.00",
            "acct_manager_commission_amt": "250.00",
            "referral_commission_amt": "125.00",
        },
        "coverages": [
            {
                "coverage_type": "Auto Liability",
                "limits": "$1,000,000",
                "deductible": "5000.00",
            }
        ],
    }

    response = api_client.post(url, payload, format="json")
    assert response.status_code == 201

    policy = Policy.objects.get(policy_number="POL-123")
    assert policy.client == client
    assert policy.producer == producer
    assert policy.account_manager == account_manager
    assert policy.referral_company == referral_company
    assert policy.financials.latest_pure_premium == Decimal(payload["financials"]["latest_pure_premium"])
    assert policy.coverages.count() == 1


@pytest.mark.django_db
def test_list_policies_returns_expected_payload(api_client, user, client, carrier_product, referral_company, lookup_values):
    api_client.force_authenticate(user=user)
    policy = Policy.objects.create(
        client=client,
        policy_number="POL-001",
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
    Coverage.objects.create(policy=policy, coverage_type="Auto Liability", limits="$1,000,000")

    url = reverse("policies:policy-list")
    response = api_client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert data["results"][0]["policy_number"] == "POL-001"
    assert data["results"][0]["coverages"][0]["coverage_type"] == "Auto Liability"


@pytest.mark.django_db
def test_soft_delete_policy_marks_related_records_inactive(api_client, user, client, carrier_product, referral_company, lookup_values):
    api_client.force_authenticate(user=user)
    policy = Policy.objects.create(
        client=client,
        policy_number="POL-321",
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
    Coverage.objects.create(policy=policy, coverage_type="Auto Liability", limits="$1,000,000")

    url = reverse("policies:policy-detail", args=[policy.id])
    response = api_client.delete(url)
    assert response.status_code == 204

    policy.refresh_from_db()
    assert policy.is_active is False
    assert policy.coverages.filter(is_active=True).count() == 0
