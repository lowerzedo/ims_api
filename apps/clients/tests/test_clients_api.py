import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.clients.models import Address, Client, ClientAddress, ClientDBA, Contact
from apps.lookups.models import AddressType, ContactType


@pytest.fixture
def api_client(db):
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(email="user@example.com", password="password123")


@pytest.fixture
def contact_type(db):
    contact_type = ContactType.objects.filter(is_active=True).first()
    assert contact_type is not None, "Expected seeded contact types"
    return contact_type


@pytest.fixture
def address_type(db):
    address_type = AddressType.objects.filter(is_active=True).first()
    assert address_type is not None, "Expected seeded address types"
    return address_type


@pytest.mark.django_db
def test_create_client_with_nested_data(api_client, user, contact_type, address_type):
    api_client.force_authenticate(user=user)
    url = reverse("clients:client-list")
    payload = {
        "company_name": "Acme Logistics",
        "dot_number": "123456",
        "fein": "12-3456789",
        "dbas": [{"dba_name": "Acme Freight"}],
        "contacts": [
            {
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "jane@example.com",
                "phone_number": "555-0100",
                "nickname": "JD",
                "contact_type_id": str(contact_type.id),
            }
        ],
        "addresses": [
            {
                "address": {
                    "street_address": "123 Main St",
                    "city": "Austin",
                    "state": "TX",
                    "zip_code": "78701",
                },
                "address_type_id": str(address_type.id),
                "rating": 5,
            }
        ],
    }

    response = api_client.post(url, payload, format="json")
    assert response.status_code == 201

    client = Client.objects.get(company_name="Acme Logistics")
    assert client.dbas.count() == 1
    assert client.contacts.count() == 1
    assert client.addresses.count() == 1


@pytest.mark.django_db
def test_list_clients_returns_payload(api_client, user, contact_type, address_type):
    api_client.force_authenticate(user=user)
    client = Client.objects.create(company_name="Acme Logistics", created_by=user, updated_by=user)
    ClientDBA.objects.create(client=client, dba_name="Acme Freight")
    Contact.objects.create(
        client=client,
        first_name="Jane",
        last_name="Doe",
        contact_type=contact_type,
    )
    url = reverse("clients:client-list")
    response = api_client.get(url)
    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 1
    assert payload["results"][0]["company_name"] == "Acme Logistics"


@pytest.mark.django_db
def test_partial_update_preserves_existing_relationships(api_client, user, contact_type, address_type):
    api_client.force_authenticate(user=user)
    client = Client.objects.create(company_name="Acme Logistics", created_by=user, updated_by=user)
    dba = ClientDBA.objects.create(client=client, dba_name="Acme Freight")
    contact = Contact.objects.create(
        client=client,
        first_name="Jane",
        last_name="Doe",
        email="jane@example.com",
        contact_type=contact_type,
    )
    address = Address.objects.create(
        street_address="123 Main St",
        city="Austin",
        state="TX",
        zip_code="78701",
    )
    client_address = ClientAddress.objects.create(
        client=client,
        address=address,
        address_type=address_type,
        rating=3,
    )

    url = reverse("clients:client-detail", args=[client.id])
    payload = {
        "dbas": [
            {
                "id": str(dba.id),
                "dba_name": "Acme Freight LLC",
            }
        ],
        "contacts": [
            {
                "id": str(contact.id),
                "first_name": "Janet",
                "contact_type_id": str(contact_type.id),
            }
        ],
        "addresses": [
            {
                "id": str(client_address.id),
                "rating": 4,
                "address": {
                    "street_address": "123 Main St",
                    "city": "Austin",
                    "state": "TX",
                    "zip_code": "78701",
                },
            }
        ],
    }

    response = api_client.patch(url, payload, format="json")
    assert response.status_code == 200

    client.refresh_from_db()
    dba.refresh_from_db()
    contact.refresh_from_db()
    client_address.refresh_from_db()

    assert dba.dba_name == "Acme Freight LLC"
    assert contact.first_name == "Janet"
    assert contact.last_name == "Doe"
    assert client_address.rating == 4


@pytest.mark.django_db
def test_search_and_filter_clients(api_client, user, contact_type, address_type):
    api_client.force_authenticate(user=user)
    acme = Client.objects.create(company_name="Acme Logistics", dot_number="123456", created_by=user, updated_by=user)
    beta = Client.objects.create(company_name="Beta Transport", dot_number="654321", created_by=user, updated_by=user)
    Contact.objects.create(client=acme, first_name="Jane", contact_type=contact_type)

    url = reverse("clients:client-list")
    response = api_client.get(url, {"search": "Acme"})
    assert response.status_code == 200
    assert response.json()["count"] == 1

    response = api_client.get(url, {"dot_number": "654321"})
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 1
    assert data["results"][0]["company_name"] == "Beta Transport"


@pytest.mark.django_db
def test_soft_delete_client(api_client, user, contact_type, address_type):
    api_client.force_authenticate(user=user)
    client = Client.objects.create(company_name="Acme Logistics", created_by=user, updated_by=user)
    url = reverse("clients:client-detail", args=[client.id])

    response = api_client.delete(url)
    assert response.status_code == 204

    client.refresh_from_db()
    assert client.is_active is False

    list_url = reverse("clients:client-list")
    response = api_client.get(list_url)
    assert response.json()["count"] == 0

    response = api_client.get(list_url, {"include_inactive": "true"})
    assert response.json()["count"] == 1
