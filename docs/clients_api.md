# Clients API Documentation

## Overview

The Clients API manages client organizations, their contacts, DBAs (Doing Business As names), and addresses.

**Base URL:** `/api/v1/clients/`

**Authentication:** All endpoints require JWT Bearer token authentication.

---

## Clients

### List Clients
```
GET /api/v1/clients/
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `dot_number` | string | Filter by DOT number (exact or contains) |
| `dot_number__icontains` | string | Partial match on DOT number |
| `fein` | string | Filter by FEIN (exact or contains) |
| `fein__icontains` | string | Partial match on FEIN |
| `contacts__contact_type` | uuid | Filter by contact type |
| `created_by` | uuid | Filter by creator user ID |
| `search` | string | Search across company name, DOT, FEIN, referral source, DBA names, contact names |
| `ordering` | string | Sort by: `company_name`, `created_at`, `updated_at` (prefix `-` for desc) |
| `include_inactive` | string | Include soft-deleted: `true`, `1`, or `yes` |
| `page` | integer | Page number (default: 1) |

**Response:** `200 OK`
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "company_name": "Acme Logistics",
      "dot_number": "123456",
      "fein": "12-3456789",
      "date_of_authority": "2020-01-15",
      "referral_source": "Web Search",
      "factoring_company": "Quick Pay Inc",
      "dbas": [
        {
          "id": "uuid",
          "dba_name": "Acme Freight",
          "is_active": true
        }
      ],
      "contacts": [
        {
          "id": "uuid",
          "first_name": "Jane",
          "last_name": "Doe",
          "email": "jane@example.com",
          "phone_number": "555-0100",
          "nickname": "JD",
          "contact_type": {
            "id": 1,
            "name": "Primary",
            "is_active": true
          },
          "is_active": true
        }
      ],
      "addresses": [
        {
          "id": "uuid",
          "address": {
            "id": "uuid",
            "street_address": "123 Main St",
            "city": "Austin",
            "state": "TX",
            "zip_code": "78701"
          },
          "address_type": {
            "id": 1,
            "name": "Physical",
            "is_active": true
          },
          "rating": 5,
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

### Create Client
```
POST /api/v1/clients/
```

**Request Body:**
```json
{
  "company_name": "Acme Logistics",
  "dot_number": "123456",
  "fein": "12-3456789",
  "date_of_authority": "2020-01-15",
  "referral_source": "Web Search",
  "factoring_company": "Quick Pay Inc",
  "dbas": [
    {
      "dba_name": "Acme Freight"
    }
  ],
  "contacts": [
    {
      "first_name": "Jane",
      "last_name": "Doe",
      "email": "jane@example.com",
      "phone_number": "555-0100",
      "nickname": "JD",
      "contact_type_id": "uuid"
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
      "address_type_id": "uuid",
      "rating": 5
    }
  ]
}
```

**Required Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `company_name` | string | Company name (max 255 chars) |

**Optional Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `dot_number` | string | DOT number (max 32 chars) |
| `fein` | string | Federal Employer ID (max 32 chars) |
| `date_of_authority` | date | Date of authority (YYYY-MM-DD) |
| `referral_source` | string | Referral source (max 255 chars) |
| `factoring_company` | string | Factoring company name (max 255 chars) |
| `dbas` | array | List of DBA entries |
| `contacts` | array | List of contact entries |
| `addresses` | array | List of address entries |

**Nested Object: DBA**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `dba_name` | string | Yes | DBA name (max 255 chars) |

**Nested Object: Contact**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `first_name` | string | Yes | First name (max 150 chars) |
| `last_name` | string | No | Last name (max 150 chars) |
| `email` | string | No | Email address |
| `phone_number` | string | No | Phone number (max 32 chars) |
| `nickname` | string | No | Nickname (max 128 chars) |
| `contact_type_id` | uuid | Yes | Contact type lookup ID |

**Nested Object: Address**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `address` | object | Yes | Address details |
| `address.street_address` | string | Yes | Street address (max 255 chars) |
| `address.city` | string | Yes | City (max 128 chars) |
| `address.state` | string | Yes | 2-letter state code |
| `address.zip_code` | string | Yes | ZIP code (max 10 chars) |
| `address_type_id` | uuid | Yes | Address type lookup ID |
| `rating` | integer | No | 1-5 rating (for garaging addresses) |

**Response:** `201 Created`

---

### Retrieve Client
```
GET /api/v1/clients/{id}/
```

**Response:** `200 OK` - Same structure as list item

---

### Update Client (Full)
```
PUT /api/v1/clients/{id}/
```

Replaces all nested arrays (dbas, contacts, addresses) with provided data.

**Request Body:** Same as create

**Response:** `200 OK`

---

### Update Client (Partial)
```
PATCH /api/v1/clients/{id}/
```

Updates only provided fields. For nested arrays, include `id` to update existing items:

```json
{
  "company_name": "Updated Company Name",
  "dbas": [
    {
      "id": "existing-dba-uuid",
      "dba_name": "Updated DBA Name"
    },
    {
      "dba_name": "New DBA"
    }
  ],
  "contacts": [
    {
      "id": "existing-contact-uuid",
      "first_name": "Updated Name",
      "contact_type_id": "uuid"
    }
  ],
  "addresses": [
    {
      "id": "existing-address-uuid",
      "rating": 4,
      "address": {
        "street_address": "456 New St",
        "city": "Austin",
        "state": "TX",
        "zip_code": "78702"
      }
    }
  ]
}
```

**Response:** `200 OK`

---

### Delete Client (Soft Delete)
```
DELETE /api/v1/clients/{id}/
```

Soft deletes the client and all related DBAs, contacts, and addresses by setting `is_active = false`.

**Response:** `204 No Content`

---

## Required Lookups

Before creating clients, fetch these lookup values:

| Lookup | Endpoint | Used For |
|--------|----------|----------|
| Contact Types | `GET /api/v1/lookups/contact-types/` | `contact_type_id` |
| Address Types | `GET /api/v1/lookups/address-types/` | `address_type_id` |

---

## Error Responses

### 400 Bad Request
```json
{
  "company_name": ["This field is required."],
  "contacts": [
    {
      "contact_type_id": ["This field is required."]
    }
  ]
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

- All IDs are UUIDs
- All datetime fields are in ISO 8601 format (UTC)
- Soft deletes preserve data - use `include_inactive=true` to view deleted records
- The `created_by` and `updated_by` fields are auto-populated from the authenticated user
- Address `rating` is used for garaging addresses (1-5 scale)
- Client-DBA combination must be unique
- Client-Address-AddressType combination must be unique

