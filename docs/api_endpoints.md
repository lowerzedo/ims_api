# IMS API Endpoint Guide

This document summarizes the endpoints currently available in the IMS backend so frontend developers can understand how to authenticate, retrieve reference data, and work with client records.

## Authentication

| Endpoint | Method | Auth required | Description |
|----------|--------|---------------|-------------|
| `/api/auth/token/` | POST | No | Obtain an access/refresh token pair using user credentials. |
| `/api/auth/token/refresh/` | POST | No | Refresh an access token using a valid refresh token. |

### Obtain Token

```http
POST /api/auth/token/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

Successful responses include `access` and `refresh` JWTs:

```json
{
  "access": "<jwt>",
  "refresh": "<jwt>"
}
```

Send the `access` token with subsequent requests using the header `Authorization: Bearer <token>`.

To refresh an access token:

```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "<jwt>"
}
```

## Health Check

| Endpoint | Method | Auth required | Description |
|----------|--------|---------------|-------------|
| `/api/health/` | GET | No | Simple availability check returning `{ "status": "ok" }`. Useful for probes/monitors. |

## Lookup Data (Read-Only)

All lookup endpoints are unauthenticated and return paginated, alphabetized data. Only active records are included.

Base path: `/api/v1/lookups/`

| Resource | Endpoint |
|----------|----------|
| Policy Statuses | `/api/v1/lookups/policy-statuses/` |
| Business Types | `/api/v1/lookups/business-types/` |
| Insurance Types | `/api/v1/lookups/insurance-types/` |
| Policy Types | `/api/v1/lookups/policy-types/` |
| Finance Companies | `/api/v1/lookups/finance-companies/` |
| Contact Types | `/api/v1/lookups/contact-types/` |
| Address Types | `/api/v1/lookups/address-types/` |
| Vehicle Types | `/api/v1/lookups/vehicle-types/` |
| License Classes | `/api/v1/lookups/license-classes/` |
| Document Types | `/api/v1/lookups/document-types/` |

Each endpoint supports `GET` with standard DRF pagination. Example response:

```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    { "id": "...", "name": "Active", "description": "Policy currently in force.", "is_active": true }
  ]
}
```

## Client API

Base path: `/api/v1/clients/`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/clients/` | GET | List clients (auth required). Supports filtering, searching, and ordering (see below). |
| `/api/v1/clients/` | POST | Create a client with optional nested DBAs, contacts, and addresses. |
| `/api/v1/clients/{id}/` | GET | Retrieve a single client with nested data. |
| `/api/v1/clients/{id}/` | PATCH | Partially update client and nested items (requires IDs for existing nested objects). |
| `/api/v1/clients/{id}/` | PUT | Replace the client payload and nested items. |
| `/api/v1/clients/{id}/` | DELETE | Soft-delete the client and mark nested records inactive (no hard delete). |

### Client Payload Structure

```json
{
  "company_name": "Acme Logistics",
  "dot_number": "123456",
  "fein": "12-3456789",
  "date_of_authority": "2024-01-01",
  "referral_source": "Referral Partner",
  "factoring_company": "Acme Financing",
  "dbas": [
    { "dba_name": "Acme Freight" }
  ],
  "contacts": [
    {
      "first_name": "Jane",
      "last_name": "Doe",
      "email": "jane@example.com",
      "phone_number": "555-0100",
      "nickname": "JD",
      "contact_type_id": "<lookup_contact_type_uuid>"
    }
  ],
  "addresses": [
    {
      "address": {
        "street_address": "123 Main St",
        "city": "Austin",
        "state": "TX",
        "zip_code": "78701"
      },
      "address_type_id": "<lookup_address_type_uuid>",
      "rating": 5
    }
  ]
}
```

Nested items return their generated `id` values. Use those IDs when performing partial updates so the serializer updates existing records rather than creating new ones:

```json
{
  "dbas": [
    { "id": "<existing_dba_id>", "dba_name": "Acme Freight LLC" }
  ],
  "contacts": [
    { "id": "<existing_contact_id>", "first_name": "Janet", "contact_type_id": "<lookup_uuid>" }
  ],
  "addresses": [
    {
      "id": "<existing_client_address_id>",
      "rating": 4,
      "address": {
        "street_address": "123 Main St",
        "city": "Austin",
        "state": "TX",
        "zip_code": "78701"
      }
    }
  ]
}
```

If a nested collection is omitted in a PATCH request, it remains untouched. Sending an empty list clears the association when performing full updates.

### Filtering & Searching

- **Search** (`GET /api/v1/clients/?search=<term>`): case-insensitive against company name, DOT, FEIN, referral_source, DBA names, and contact names.
- **Filter** parameters:
  - `dot_number`: exact or `icontains` (e.g., `?dot_number=123456` or `?dot_number__icontains=123`).
  - `fein`: exact or `icontains` (e.g., `?fein__icontains=12-34`).
  - `contacts__contact_type`: filter by lookup contact type UUID.
  - `created_by`: filter by creator user UUID.
- **Ordering** (`?ordering=company_name` or `?ordering=-created_at`). Defaults to company name ascending.
- **Inactive records**: by default only `is_active=true` clients are returned. Include `?include_inactive=true` to see soft-deleted rows.

### Soft Delete Behaviour

`DELETE /api/v1/clients/{id}/` sets `is_active=false` on the client and cascades the inactive flag to related DBAs, contacts, and addresses. Physical rows remain in the database so history can be preserved. Subsequent list calls must opt in to inactive records with `?include_inactive=true`.

---

As new resources (policies, assets, etc.) come online, extend this document so the frontend team always has a single reference for endpoint behaviour and payload expectations.
