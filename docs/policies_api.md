# Policies API Documentation

## Overview

The Policies API manages insurance policies, carrier products, general agents, referral companies, and policy financials.

**Base URL:** `/api/v1/policies/`

**Authentication:** All endpoints require JWT Bearer token authentication.

---

## Policies

### List Policies
```
GET /api/v1/policies/policies/
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `client` | uuid | Filter by client ID |
| `status` | uuid | Filter by policy status lookup ID |
| `business_type` | uuid | Filter by business type ID |
| `insurance_type` | uuid | Filter by insurance type ID |
| `policy_type` | uuid | Filter by policy type ID |
| `carrier_product` | uuid | Filter by carrier product ID |
| `finance_company` | uuid | Filter by finance company ID |
| `producer` | uuid | Filter by producer user ID |
| `account_manager` | uuid | Filter by account manager user ID |
| `referral_company` | uuid | Filter by referral company ID |
| `effective_date` | date | Exact effective date |
| `effective_date__gte` | date | Effective date on or after |
| `effective_date__lte` | date | Effective date on or before |
| `search` | string | Search policy number, client name, carrier name, GA name |
| `ordering` | string | Sort: `policy_number`, `effective_date`, `maturity_date`, `created_at`, `updated_at` |
| `include_inactive` | string | Include soft-deleted: `true`, `1`, or `yes` |
| `page` | integer | Page number |

**Response:** `200 OK`
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "client": {
        "id": "uuid",
        "company_name": "Acme Logistics"
      },
      "policy_number": "POL-2025-001",
      "status": {
        "id": 1,
        "name": "Active",
        "is_active": true
      },
      "business_type": {
        "id": 1,
        "name": "Trucking",
        "is_active": true
      },
      "insurance_type": {
        "id": 1,
        "name": "Commercial Auto",
        "is_active": true
      },
      "policy_type": {
        "id": 1,
        "name": "New Business",
        "is_active": true
      },
      "effective_date": "2025-01-01",
      "maturity_date": "2026-01-01",
      "carrier_product": {
        "id": "uuid",
        "line_of_business": "Commercial Auto",
        "general_agent": {
          "id": "uuid",
          "name": "ABC General Agency",
          "agency_commission": "15.00",
          "is_active": true,
          "created_at": "...",
          "updated_at": "..."
        },
        "insurance_company_name": "Great Insurance Co",
        "abbreviation": "GIC",
        "new_business_commission_pct": "12.00",
        "renewal_commission_pct": "10.00",
        "is_retained": false,
        "is_premium_financed": true,
        "has_sweep_down": false,
        "has_sweep_payment": false,
        "has_auto_renew": true,
        "naic_code": "12345",
        "am_best_number": "001234",
        "am_best_rating": "A+",
        "is_active": true,
        "created_at": "...",
        "updated_at": "..."
      },
      "finance_company": {
        "id": 1,
        "name": "Premium Finance Corp",
        "is_active": true
      },
      "producer": {
        "id": "uuid",
        "email": "producer@example.com",
        "first_name": "John",
        "last_name": "Smith",
        "role": "producer"
      },
      "account_manager": {
        "id": "uuid",
        "email": "am@example.com",
        "first_name": "Sarah",
        "last_name": "Jones",
        "role": "account_manager"
      },
      "producer_rate": "12.00",
      "account_manager_rate": "9.50",
      "referral_company": {
        "id": "uuid",
        "name": "Referral Partners LLC",
        "rate": "5.00",
        "is_active": true,
        "created_at": "...",
        "updated_at": "..."
      },
      "financials": {
        "id": "uuid",
        "original_pure_premium": "10000.00",
        "latest_pure_premium": "10500.00",
        "broker_fee": "500.00",
        "taxes": "315.00",
        "agency_fee": "150.00",
        "total_premium": "11465.00",
        "down_payment": "2500.00",
        "acct_manager_commission_amt": "997.50",
        "referral_commission_amt": "525.00",
        "is_active": true,
        "created_at": "...",
        "updated_at": "..."
      },
      "coverages": [
        {
          "id": "uuid",
          "coverage_type": "Liability",
          "limits": "$1,000,000 CSL",
          "deductible": "1000.00",
          "is_active": true
        }
      ],
      "is_active": true,
      "created_at": "2025-11-26T10:00:00Z",
      "updated_at": "2025-11-26T10:00:00Z"
    }
  ]
}
```

---

### Create Policy
```
POST /api/v1/policies/policies/
```

**Request Body:**
```json
{
  "client_id": "uuid",
  "policy_number": "POL-2025-001",
  "status_id": 1,
  "business_type_id": 1,
  "insurance_type_id": 1,
  "policy_type_id": 1,
  "effective_date": "2025-01-01",
  "maturity_date": "2026-01-01",
  "carrier_product_id": "uuid",
  "finance_company_id": 1,
  "producer_id": "uuid",
  "producer_rate": "12.00",
  "account_manager_id": "uuid",
  "account_manager_rate": "9.50",
  "referral_company_id": "uuid",
  "financials": {
    "original_pure_premium": "10000.00",
    "latest_pure_premium": "10000.00",
    "broker_fee": "500.00",
    "taxes": "315.00",
    "agency_fee": "150.00",
    "total_premium": "10965.00",
    "down_payment": "2500.00",
    "acct_manager_commission_amt": "950.00",
    "referral_commission_amt": "500.00"
  },
  "coverages": [
    {
      "coverage_type": "Liability",
      "limits": "$1,000,000 CSL",
      "deductible": "1000.00"
    }
  ]
}
```

**Required Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `client_id` | uuid | Client ID |
| `policy_number` | string | Policy number (max 128 chars) |
| `status_id` | integer | Policy status lookup ID |
| `business_type_id` | integer | Business type lookup ID |
| `insurance_type_id` | integer | Insurance type lookup ID |
| `policy_type_id` | integer | Policy type lookup ID |
| `effective_date` | date | Policy effective date |
| `maturity_date` | date | Policy maturity/expiration date |
| `carrier_product_id` | uuid | Carrier product ID |

**Optional Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `finance_company_id` | integer | Finance company lookup ID |
| `producer_id` | uuid | Producer user ID |
| `account_manager_id` | uuid | Account manager user ID |
| `account_manager_rate` | decimal | AM commission rate (0.00-100.00) |
| `referral_company_id` | uuid | Referral company ID |
| `financials` | object | Policy financial details |
| `coverages` | array | Coverage line items |

**Nested Object: Financials**
| Field | Type | Description |
|-------|------|-------------|
| `original_pure_premium` | decimal | Original pure premium |
| `latest_pure_premium` | decimal | Current pure premium |
| `broker_fee` | decimal | Broker fee amount |
| `taxes` | decimal | Tax amount |
| `agency_fee` | decimal | Agency fee amount |
| `total_premium` | decimal | Total premium amount |
| `down_payment` | decimal | Down payment amount |
| `acct_manager_commission_amt` | decimal | Account manager commission |
| `referral_commission_amt` | decimal | Referral commission |

**Nested Object: Coverage**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `coverage_type` | string | Yes | Coverage type (max 128 chars) |
| `limits` | string | No | Coverage limits description |
| `deductible` | decimal | No | Deductible amount |

**Response:** `201 Created`

---

### Update Policy
```
PUT /api/v1/policies/policies/{id}/
PATCH /api/v1/policies/policies/{id}/
```

For partial updates, include `id` in coverages to update existing:
```json
{
  "coverages": [
    {
      "id": "existing-coverage-uuid",
      "limits": "$2,000,000 CSL"
    }
  ]
}
```

**Response:** `200 OK`

---

### Delete Policy (Soft Delete)
```
DELETE /api/v1/policies/policies/{id}/
```

Soft deletes policy, financials, and all coverages.

**Response:** `204 No Content`

---

## General Agents

### List General Agents
```
GET /api/v1/policies/general-agents/
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `search` | string | Search by name |
| `ordering` | string | Sort: `name`, `created_at` |
| `include_inactive` | string | Include soft-deleted |

**Response:** `200 OK`
```json
{
  "count": 1,
  "results": [
    {
      "id": "uuid",
      "name": "ABC General Agency",
      "agency_commission": "15.00",
      "is_active": true,
      "created_at": "...",
      "updated_at": "..."
    }
  ]
}
```

### Create General Agent
```
POST /api/v1/policies/general-agents/
```

**Request Body:**
```json
{
  "name": "ABC General Agency",
  "agency_commission": "15.00"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique name (max 255 chars) |
| `agency_commission` | decimal | No | Commission % (default 0.00) |

**Response:** `201 Created`

---

## Carrier Products

### List Carrier Products
```
GET /api/v1/policies/carrier-products/
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `search` | string | Search company name, line of business, GA name |
| `ordering` | string | Sort: `insurance_company_name`, `line_of_business`, `created_at` |
| `include_inactive` | string | Include soft-deleted |

### Create Carrier Product
```
POST /api/v1/policies/carrier-products/
```

**Request Body:**
```json
{
  "line_of_business": "Commercial Auto",
  "general_agent_id": "uuid",
  "insurance_company_name": "Great Insurance Co",
  "abbreviation": "GIC",
  "new_business_commission_pct": "12.00",
  "renewal_commission_pct": "10.00",
  "is_retained": false,
  "is_premium_financed": true,
  "has_sweep_down": false,
  "has_sweep_payment": false,
  "has_auto_renew": true,
  "naic_code": "12345",
  "am_best_number": "001234",
  "am_best_rating": "A+"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `line_of_business` | string | Yes | Line of business (max 128 chars) |
| `insurance_company_name` | string | Yes | Insurance company name (max 255 chars) |
| `general_agent_id` | uuid | No | General agent ID |
| `abbreviation` | string | No | Short name (max 64 chars) |
| `new_business_commission_pct` | decimal | No | New business commission % |
| `renewal_commission_pct` | decimal | No | Renewal commission % |
| `is_retained` | boolean | No | Is retained (default false) |
| `is_premium_financed` | boolean | No | Is premium financed (default false) |
| `has_sweep_down` | boolean | No | Has sweep down (default false) |
| `has_sweep_payment` | boolean | No | Has sweep payment (default false) |
| `has_auto_renew` | boolean | No | Has auto renew (default false) |
| `naic_code` | string | No | NAIC code (max 32 chars) |
| `am_best_number` | string | No | AM Best number (max 32 chars) |
| `am_best_rating` | string | No | AM Best rating (max 32 chars) |

**Note:** Combination of `insurance_company_name` + `line_of_business` must be unique.

**Response:** `201 Created`

---

## Referral Companies

### List Referral Companies
```
GET /api/v1/policies/referral-companies/
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `search` | string | Search by name |
| `ordering` | string | Sort: `name`, `created_at` |
| `include_inactive` | string | Include soft-deleted |

### Create Referral Company
```
POST /api/v1/policies/referral-companies/
```

**Request Body:**
```json
{
  "name": "Referral Partners LLC",
  "rate": "5.00"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Unique name (max 255 chars) |
| `rate` | decimal | No | Referral commission % (default 0.00) |

**Response:** `201 Created`

---

## Required Lookups

Before creating policies, fetch these lookup values:

| Lookup | Endpoint |
|--------|----------|
| Policy Statuses | `GET /api/v1/lookups/policy-statuses/` |
| Business Types | `GET /api/v1/lookups/business-types/` |
| Insurance Types | `GET /api/v1/lookups/insurance-types/` |
| Policy Types | `GET /api/v1/lookups/policy-types/` |
| Finance Companies | `GET /api/v1/lookups/finance-companies/` |

---

## Error Responses

### 400 Bad Request
```json
{
  "policy_number": ["This field is required."],
  "client_id": ["Invalid pk \"invalid-uuid\" - object does not exist."]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

---

## Notes

- Policy number + client combination must be unique
- `account_manager_rate` is a percentage (0-100)
- All decimal fields use 2 decimal places
- Financial calculations are stored, not computed server-side
- Soft deletes cascade to financials and coverages

