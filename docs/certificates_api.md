# Certificates API Documentation

## Overview

The Certificates API manages certificate holders, master certificate templates, and issued certificates of insurance.

**Base URL:** `/api/v1/certificates/`

**Authentication:** All endpoints require JWT Bearer token authentication.

---

## Certificate Holders

Entities that receive certificates (e.g., loss payees, additional insureds).

### List Certificate Holders
```
GET /api/v1/certificates/certificate-holders/
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `search` | string | Search name, contact person, city, state |
| `ordering` | string | Sort: `name`, `created_at` |
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
      "name": "ABC Warehouse Inc",
      "email": "insurance@abcwarehouse.com",
      "contact_person": "John Smith",
      "phone_number": "555-123-4567",
      "address": {
        "id": "uuid",
        "street_address": "500 Industrial Blvd",
        "city": "Houston",
        "state": "TX",
        "zip_code": "77001"
      },
      "is_active": true,
      "created_at": "2025-11-26T10:00:00Z",
      "updated_at": "2025-11-26T10:00:00Z"
    }
  ]
}
```

---

### Create Certificate Holder
```
POST /api/v1/certificates/certificate-holders/
```

**Request Body:**
```json
{
  "name": "ABC Warehouse Inc",
  "email": "insurance@abcwarehouse.com",
  "contact_person": "John Smith",
  "phone_number": "555-123-4567",
  "address": {
    "street_address": "500 Industrial Blvd",
    "city": "Houston",
    "state": "TX",
    "zip_code": "77001"
  }
}
```

**Required Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Holder name (max 255 chars) |
| `address` | object | Address details |
| `address.street_address` | string | Street address (max 255 chars) |
| `address.city` | string | City (max 128 chars) |
| `address.state` | string | 2-letter state code |
| `address.zip_code` | string | ZIP code (max 10 chars) |

**Optional Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `email` | string | Email address |
| `contact_person` | string | Contact person name (max 255 chars) |
| `phone_number` | string | Phone number (max 32 chars) |

**Response:** `201 Created`

---

### Update Certificate Holder
```
PUT /api/v1/certificates/certificate-holders/{id}/
PATCH /api/v1/certificates/certificate-holders/{id}/
```

**Response:** `200 OK`

---

### Delete Certificate Holder (Soft Delete)
```
DELETE /api/v1/certificates/certificate-holders/{id}/
```

**Response:** `204 No Content`

---

## Master Certificates

Reusable templates that drive generated certificates for a policy.

### List Master Certificates
```
GET /api/v1/certificates/master-certificates/
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `policy` | uuid | Filter by policy ID |
| `search` | string | Search name, policy number, client company name |
| `ordering` | string | Sort: `name`, `created_at`, `updated_at` |
| `include_inactive` | string | Include soft-deleted |
| `page` | integer | Page number |

**Response:** `200 OK`
```json
{
  "count": 1,
  "results": [
    {
      "id": "uuid",
      "policy": {
        "id": "uuid",
        "policy_number": "POL-2025-001"
      },
      "name": "Standard COI Template",
      "settings": {
        "show_vehicles": true,
        "show_drivers": true,
        "additional_insured_wording": "Named as additional insured..."
      },
      "created_by": {
        "id": "uuid",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "account_manager"
      },
      "updated_by": {...},
      "is_active": true,
      "created_at": "2025-11-26T10:00:00Z",
      "updated_at": "2025-11-26T10:00:00Z"
    }
  ]
}
```

---

### Create Master Certificate
```
POST /api/v1/certificates/master-certificates/
```

**Request Body:**
```json
{
  "policy_id": "uuid",
  "name": "Standard COI Template",
  "settings": {
    "show_vehicles": true,
    "show_drivers": true,
    "additional_insured_wording": "Named as additional insured..."
  }
}
```

**Required Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `policy_id` | uuid | Policy ID |
| `name` | string | Template name (max 255 chars) |

**Optional Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `settings` | object | JSON configuration for certificate generation |

**Note:** Policy + name combination must be unique.

**Response:** `201 Created`

---

### Update Master Certificate
```
PUT /api/v1/certificates/master-certificates/{id}/
PATCH /api/v1/certificates/master-certificates/{id}/
```

**Response:** `200 OK`

---

### Delete Master Certificate (Soft Delete)
```
DELETE /api/v1/certificates/master-certificates/{id}/
```

**Response:** `204 No Content`

---

## Certificates

Issued certificates of insurance derived from master templates.

### List Certificates
```
GET /api/v1/certificates/certificates/
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `master_certificate` | uuid | Filter by master certificate ID |
| `master_certificate__policy` | uuid | Filter by policy ID |
| `certificate_holder` | uuid | Filter by certificate holder ID |
| `search` | string | Search verification code, master name, policy number, holder name |
| `ordering` | string | Sort: `created_at`, `updated_at` |
| `include_inactive` | string | Include soft-deleted |
| `page` | integer | Page number |

**Response:** `200 OK`
```json
{
  "count": 1,
  "results": [
    {
      "id": "uuid",
      "master_certificate": {
        "id": "uuid",
        "policy": {
          "id": "uuid",
          "policy_number": "POL-2025-001"
        },
        "name": "Standard COI Template",
        "settings": {...},
        "created_by": {...},
        "updated_by": {...},
        "is_active": true,
        "created_at": "...",
        "updated_at": "..."
      },
      "certificate_holder": {
        "id": "uuid",
        "name": "ABC Warehouse Inc",
        "email": "insurance@abcwarehouse.com",
        "contact_person": "John Smith",
        "phone_number": "555-123-4567",
        "address": {...},
        "is_active": true,
        "created_at": "...",
        "updated_at": "..."
      },
      "verification_code": "ABC123XYZ789",
      "document": "https://example.com/media/certificates/.../certificate-ABC123XYZ789.pdf",
      "vehicles": [
        {
          "id": "uuid",
          "vin": "1HGCM82633A123456",
          "unit_number": "TRUCK-001",
          "year": 2023,
          "make": "Freightliner",
          "model": "Cascadia",
          "pd_amount": "125000.00"
        }
      ],
      "drivers": [
        {
          "id": "uuid",
          "first_name": "John",
          "last_name": "Doe",
          "license_number": "D1234567",
          "license_state": "TX",
          "hire_date": "2022-06-01"
        }
      ],
      "created_by": {
        "id": "uuid",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "account_manager"
      },
      "updated_by": {...},
      "is_active": true,
      "created_at": "2025-11-26T10:00:00Z",
      "updated_at": "2025-11-26T10:00:00Z"
    }
  ]
}
```

---

### Create Certificate
```
POST /api/v1/certificates/certificates/
```

**Request Body:**
```json
{
  "master_certificate_id": "uuid",
  "certificate_holder_id": "uuid",
  "vehicle_ids": ["uuid", "uuid"],
  "driver_ids": ["uuid", "uuid"]
}
```

**Required Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `master_certificate_id` | uuid | Master certificate template ID |
| `certificate_holder_id` | uuid | Certificate holder ID |

**Optional Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `vehicle_ids` | array | List of vehicle UUIDs to include |
| `driver_ids` | array | List of driver UUIDs to include |

**Validation:**
- Vehicles must belong to the policy's client
- Drivers must belong to the policy's client

**Auto-generated:**
- `verification_code` - 12-character unique code (uppercase alphanumeric)
- `document` - PDF file generated upon creation

**Response:** `201 Created`

---

### Retrieve Certificate
```
GET /api/v1/certificates/certificates/{id}/
```

**Response:** `200 OK` - Same structure as list item

---

### Update Certificate
```
PUT /api/v1/certificates/certificates/{id}/
PATCH /api/v1/certificates/certificates/{id}/
```

**Request Body:**
```json
{
  "certificate_holder_id": "uuid",
  "vehicle_ids": ["uuid"],
  "driver_ids": ["uuid"]
}
```

**Note:** Updating a certificate regenerates the PDF document.

**Response:** `200 OK`

---

### Delete Certificate (Soft Delete)
```
DELETE /api/v1/certificates/certificates/{id}/
```

**Response:** `204 No Content`

---

## File Storage

Certificate documents are organized in the following structure:
```
media/certificates/{client_id}/{policy_id}/{certificate_id}/certificate-{verification_code}.pdf
```

Files are served via:
- **Local development:** `http://localhost:8000/media/...`
- **Production:** S3 or configured storage backend

---

## Verification Code

Each certificate has a unique 12-character verification code:
- Format: Uppercase alphanumeric (A-Z, 0-9)
- Example: `ABC123XYZ789`
- Auto-generated on creation
- Cannot be modified
- Used to verify certificate authenticity

---

## Error Responses

### 400 Bad Request
```json
{
  "master_certificate_id": ["This field is required."],
  "non_field_errors": ["Selected vehicle does not belong to the policy client."]
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

- PDF document is automatically generated/regenerated on create/update
- Vehicles and drivers must belong to the same client as the policy
- Master certificate name must be unique per policy
- `verification_code` is system-generated and read-only
- `document` URL is read-only
- `created_by` and `updated_by` are auto-populated from authenticated user

