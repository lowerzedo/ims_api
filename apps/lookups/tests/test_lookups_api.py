import pytest
from django.urls import reverse

from apps.lookups.models import PolicyStatus


pytestmark = pytest.mark.django_db


def test_policy_status_seed_data():
    names = set(PolicyStatus.objects.values_list("name", flat=True))
    assert {"Active", "Inactive", "Prospect"}.issubset(names)


def test_policy_status_endpoint_returns_active_entries(client):
    url = reverse("lookups:lookup-policy-status-list")
    response = client.get(url)
    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] >= 3
    returned_names = {item["name"] for item in payload["results"]}
    assert "Active" in returned_names
