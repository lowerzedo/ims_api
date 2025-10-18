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

## Policies API

Base path: `/api/v1/policies/`

| Endpoint | Method(s) | Description |
|----------|-----------|-------------|
| `/api/v1/policies/policies/` | `GET`, `POST` | List policies or create a new policy with nested financials and coverage lines. |
| `/api/v1/policies/policies/{id}/` | `GET`, `PATCH`, `PUT`, `DELETE` | Retrieve, update, or soft-delete a policy. Partial updates accept only changed fields while `PUT` replaces the record. |

### Policy Payload Structure

```json
{
  "client_id": "<client_uuid>",
  "policy_number": "POL-123",
  "status_id": "<lookup_policy_status_uuid>",
  "business_type_id": "<lookup_business_type_uuid>",
  "insurance_type_id": "<lookup_insurance_type_uuid>",
  "policy_type_id": "<lookup_policy_type_uuid>",
  "effective_date": "2024-01-01",
  "maturity_date": "2025-01-01",
  "carrier_product_id": "<carrier_product_uuid>",
  "finance_company_id": "<lookup_finance_company_uuid>",
  "producer_id": "<user_uuid>",
  "account_manager_id": "<user_uuid>",
  "account_manager_rate": "9.50",
  "referral_company_id": "<referral_company_uuid>",
  "financials": {
    "original_pure_premium": "10000.00",
    "latest_pure_premium": "10500.00",
    "broker_fee": "250.00",
    "taxes": "120.00",
    "agency_fee": "300.00",
    "total_premium": "11000.00",
    "down_payment": "2000.00",
    "acct_manager_commission_amt": "250.00",
    "referral_commission_amt": "125.00"
  },
  "coverages": [
    { "coverage_type": "Auto Liability", "limits": "$1,000,000", "deductible": "5000.00" }
  ]
}
```

Coverages accept existing IDs when updating:

```json
{
  "coverages": [
    { "id": "<coverage_uuid>", "limits": "$1,500,000", "deductible": "2500.00" }
  ]
}
```

`DELETE /api/v1/policies/policies/{id}/` sets `is_active=false` on the policy and its nested coverages and financial record. Include `?include_inactive=true` to browse archived policies.

### Provider Catalog Endpoints

The following helper resources live under the same base path and power dropdowns in the UI. All require authentication and support soft-deletes via `DELETE`.

| Resource | Endpoint | Method(s) | Notes |
|----------|----------|-----------|-------|
| General Agents | `/api/v1/policies/general-agents/` | `GET`, `POST` | List or create general agencies with commission defaults. |
| General Agent | `/api/v1/policies/general-agents/{id}/` | `GET`, `PATCH`, `PUT`, `DELETE` | Retrieve/update a single agency or deactivate it. |
| Carrier Products | `/api/v1/policies/carrier-products/` | `GET`, `POST` | List or create carrier offerings linked to a general agent. |
| Carrier Product | `/api/v1/policies/carrier-products/{id}/` | `GET`, `PATCH`, `PUT`, `DELETE` | Update product details or mark them inactive. |
| Referral Companies | `/api/v1/policies/referral-companies/` | `GET`, `POST` | Manage the referral partner catalog. |
| Referral Company | `/api/v1/policies/referral-companies/{id}/` | `GET`, `PATCH`, `PUT`, `DELETE` | Retrieve/update referral data or perform a soft-delete. |

All provider endpoints support `?include_inactive=true` to display soft-deleted rows, as well as `search` and `ordering` parameters where applicable.

## Assets API

Base path: `/api/v1/assets/`

| Endpoint | Method(s) | Description |
|----------|-----------|-------------|
| `/api/v1/assets/loss-payees/` | `GET`, `POST` | List loss payees or create a new one (address payload required). |
| `/api/v1/assets/loss-payees/{id}/` | `GET`, `PATCH`, `PUT`, `DELETE` | Retrieve, update, or soft-delete a loss payee. Address fields can be edited inline. |
| `/api/v1/assets/vehicles/` | `GET`, `POST` | Browse vehicles or create one. Creation requires `client_id`, `vehicle_type_id`, and VIN. |
| `/api/v1/assets/vehicles/{id}/` | `GET`, `PATCH`, `PUT`, `DELETE` | Manage a specific vehicle or mark it inactive (soft delete). |
| `/api/v1/assets/policy-vehicles/` | `GET`, `POST` | List policy assignments or attach a vehicle to a policy along with garaging address. |
| `/api/v1/assets/policy-vehicles/{id}/` | `GET`, `PATCH`, `PUT`, `DELETE` | Update assignment status/dates or soft-delete the linkage. |

### Vehicle Payload Example

```json
{
  "client_id": "<client_uuid>",
  "vin": "1XPWD40X1ED215307",
  "unit_number": "UNIT-001",
  "vehicle_type_id": "<lookup_vehicle_type_uuid>",
  "year": 2024,
  "make": "Peterbilt",
  "model": "579",
  "gvw": 80000,
  "pd_amount": "120000.00",
  "deductible": "1000.00",
  "loss_payee_id": "<optional_loss_payee_uuid>"
}
```

### Loss Payee Payload Example

```json
{
  "name": "Bank of Example",
  "email": "loss@example.com",
  "preference": "EMAIL",
  "address": {
    "street_address": "100 Main St",
    "city": "Austin",
    "state": "TX",
    "zip_code": "78701"
  }
}
```

### Policy Assignment Payload Example

```json
{
  "policy_id": "<policy_uuid>",
  "vehicle_id": "<vehicle_uuid>",
  "garaging_address_id": "<address_uuid>",
  "status": "active",
  "inception_date": "2024-02-01"
}
```

Assignments enforce uniqueness per policy/vehicle pair and return a validation error if the relationship already exists. Soft-deleted records remain hidden unless `?include_inactive=true` is supplied on list endpoints.

---

As new resources (finance, documents, etc.) come online, extend this document so the frontend team always has a single reference for endpoint behaviour and payload expectations.
