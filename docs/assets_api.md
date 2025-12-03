# Assets API Documentation

## Overview

The Assets API manages vehicles, drivers, loss payees, and their assignments to policies.

**Base URL:** `/api/v1/assets/`

**Authentication:** All endpoints require JWT Bearer token authentication.

---

## Vehicles

### List Vehicles
```
GET /api/v1/assets/vehicles/
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `client` | uuid | Filter by client ID |
| `vehicle_type` | uuid | Filter by vehicle type ID |
| `loss_payee` | uuid | Filter by loss payee ID |
| `year` | integer | Filter by exact year |
| `year__gte` | integer | Year greater than or equal |
| `year__lte` | integer | Year less than or equal |
| `search` | string | Search VIN, unit number, client name, make, model |
| `ordering` | string | Sort: `vin`, `unit_number`, `year`, `created_at`, `updated_at` |
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
      "vin": "1HGCM82633A123456",
      "unit_number": "TRUCK-001",
      "vehicle_type": {
        "id": 1,
        "name": "Tractor",
        "is_active": true
      },
      "year": 2023,
      "make": "Freightliner",
      "model": "Cascadia",
      "gvw": 80000,
      "pd_amount": "125000.00",
      "deductible": "2500.00",
      "loss_payee": {
        "id": "uuid",
        "name": "Bank of America",
        "email": "leasing@boa.com",
        "contact_person_name": "Jane Smith",
        "telephone": "800-555-1234",
        "fax": "800-555-1235",
        "cell_phone": "",
        "preference": "EMAIL",
        "remarks": "Preferred contact method is email",
        "address": {
          "id": "uuid",
          "street_address": "100 Bank St",
          "city": "Charlotte",
          "state": "NC",
          "zip_code": "28255"
        },
        "is_active": true,
        "created_at": "...",
        "updated_at": "..."
      },
      "garaging_addresses": [
        {
          "policy_id": "uuid",
          "policy_number": "POL-2025-001",
          "status": "active",
          "address": {
            "id": "uuid",
            "street_address": "123 Main St",
            "city": "Austin",
            "state": "TX",
            "zip_code": "78701"
          }
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

### Create Vehicle
```
POST /api/v1/assets/vehicles/
```

**Request Body:**
```json
{
  "client_id": "uuid",
  "vin": "1HGCM82633A123456",
  "unit_number": "TRUCK-001",
  "vehicle_type_id": 1,
  "year": 2023,
  "make": "Freightliner",
  "model": "Cascadia",
  "gvw": 80000,
  "pd_amount": "125000.00",
  "deductible": "2500.00",
  "loss_payee_id": "uuid"
}
```

**Required Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `client_id` | uuid | Client ID |
| `vin` | string | 17-character VIN (excludes I, O, Q) |
| `vehicle_type_id` | integer | Vehicle type lookup ID |
| `year` | integer | Model year (1900-2100) |
| `make` | string | Vehicle make (max 128 chars) |
| `model` | string | Vehicle model (max 128 chars) |

**Optional Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `unit_number` | string | Internal unit number (max 64 chars) |
| `gvw` | integer | Gross vehicle weight (lbs) |
| `pd_amount` | decimal | Physical damage value |
| `deductible` | decimal | Deductible amount |
| `loss_payee_id` | uuid | Loss payee ID |

**Response:** `201 Created`

---

### Update Vehicle
```
PUT /api/v1/assets/vehicles/{id}/
PATCH /api/v1/assets/vehicles/{id}/
```

**Response:** `200 OK`

---

### Delete Vehicle (Soft Delete)
```
DELETE /api/v1/assets/vehicles/{id}/
```

**Response:** `204 No Content`

---

## Policy Vehicles

Assign vehicles to policies.

### List Policy Vehicles
```
GET /api/v1/assets/policy-vehicles/
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `policy` | uuid | Filter by policy ID |
| `vehicle` | uuid | Filter by vehicle ID |
| `status` | string | Filter by status: `active`, `inactive`, `unassigned` |
| `ordering` | string | Sort: `created_at`, `updated_at`, `inception_date` |
| `include_inactive` | string | Include soft-deleted |

**Response:** `200 OK`
```json
{
  "count": 1,
  "results": [
    {
      "id": "uuid",
      "policy": "uuid",
      "vehicle": {
        "id": "uuid",
        "client": {...},
        "vin": "1HGCM82633A123456",
        "unit_number": "TRUCK-001",
        "vehicle_type": {...},
        "year": 2023,
        "make": "Freightliner",
        "model": "Cascadia",
        "gvw": 80000,
        "pd_amount": "125000.00",
        "deductible": "2500.00",
        "loss_payee": {...},
        "is_active": true,
        "created_at": "...",
        "updated_at": "..."
      },
      "status": "active",
      "inception_date": "2025-01-01",
      "termination_date": null,
      "garaging_address": {
        "id": "uuid",
        "street_address": "123 Main St",
        "city": "Austin",
        "state": "TX",
        "zip_code": "78701"
      },
      "is_active": true,
      "created_at": "...",
      "updated_at": "..."
    }
  ]
}
```

### Create Policy Vehicle
```
POST /api/v1/assets/policy-vehicles/
```

**Request Body:**
```json
{
  "policy_id": "uuid",
  "vehicle_id": "uuid",
  "status": "active",
  "inception_date": "2025-01-01",
  "termination_date": null,
  "garaging_address_id": "uuid"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `policy_id` | uuid | Yes | Policy ID |
| `vehicle_id` | uuid | Yes | Vehicle ID |
| `garaging_address_id` | uuid | Yes | Garaging address ID |
| `status` | string | No | Status (default: `active`) |
| `inception_date` | date | No | When vehicle was added |
| `termination_date` | date | No | When vehicle was removed |

**Status Values:**
- `active` - Currently on policy
- `inactive` - Removed from policy
- `unassigned` - Not yet assigned

**Error:** Returns `400` if vehicle already assigned to policy.

**Response:** `201 Created`

---

### Update Policy Vehicle
```
PUT /api/v1/assets/policy-vehicles/{id}/
PATCH /api/v1/assets/policy-vehicles/{id}/
```

Update status, dates, or garaging address. Cannot change policy or vehicle assignment.

**Request Body (PATCH):**
```json
{
  "status": "inactive",
  "termination_date": "2025-06-15"
}
```

**Updatable Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `active`, `inactive`, or `unassigned` |
| `inception_date` | date | When vehicle was added |
| `termination_date` | date | When vehicle was removed |
| `garaging_address_id` | uuid | Update garaging address |

**Response:** `200 OK`

---

### Remove Policy Vehicle (Soft Delete)
```
DELETE /api/v1/assets/policy-vehicles/{id}/
```

Soft deletes the assignment (sets `is_active = false`).

**Response:** `204 No Content`

**To view removed assignments:**
```
GET /api/v1/assets/policy-vehicles/?include_inactive=true
```

---

## Drivers

### List Drivers
```
GET /api/v1/assets/drivers/
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `client` | uuid | Filter by client ID |
| `license_class` | uuid | Filter by license class ID |
| `license_state` | string | Filter by 2-letter state code |
| `hire_date` | date | Exact hire date |
| `hire_date__gte` | date | Hire date on or after |
| `hire_date__lte` | date | Hire date on or before |
| `search` | string | Search first/last name, license number, client name |
| `ordering` | string | Sort: `last_name`, `first_name`, `created_at`, `updated_at` |
| `include_inactive` | string | Include soft-deleted |

**Response:** `200 OK`
```json
{
  "count": 1,
  "results": [
    {
      "id": "uuid",
      "client": {
        "id": "uuid",
        "company_name": "Acme Logistics"
      },
      "first_name": "John",
      "middle_name": "Robert",
      "last_name": "Doe",
      "date_of_birth": "1985-03-15",
      "license_number": "D1234567",
      "license_state": "TX",
      "license_class": {
        "id": 1,
        "name": "Class A CDL",
        "is_active": true
      },
      "issue_date": "2020-01-15",
      "hire_date": "2022-06-01",
      "violations": 0,
      "accidents": 1,
      "is_active": true,
      "created_at": "...",
      "updated_at": "..."
    }
  ]
}
```

### Create Driver
```
POST /api/v1/assets/drivers/
```

**Request Body:**
```json
{
  "client_id": "uuid",
  "first_name": "John",
  "middle_name": "Robert",
  "last_name": "Doe",
  "date_of_birth": "1985-03-15",
  "license_number": "D1234567",
  "license_state": "TX",
  "license_class_id": 1,
  "issue_date": "2020-01-15",
  "hire_date": "2022-06-01",
  "violations": 0,
  "accidents": 1
}
```

**Required Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `client_id` | uuid | Client ID |
| `first_name` | string | First name (max 150 chars) |
| `last_name` | string | Last name (max 150 chars) |
| `date_of_birth` | date | Date of birth |
| `license_number` | string | License number (max 64 chars) |
| `license_state` | string | 2-letter state code |
| `license_class_id` | integer | License class lookup ID |

**Optional Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `middle_name` | string | Middle name (max 150 chars) |
| `issue_date` | date | License issue date |
| `hire_date` | date | Employment hire date |
| `violations` | integer | Number of violations (default 0) |
| `accidents` | integer | Number of accidents (default 0) |

**Note:** Client + license_number combination must be unique.

**Response:** `201 Created`

---

## Policy Drivers

Assign drivers to policies.

### List Policy Drivers
```
GET /api/v1/assets/policy-drivers/
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `policy` | uuid | Filter by policy ID |
| `driver` | uuid | Filter by driver ID |
| `status` | string | Filter by status: `active`, `inactive`, `not_assigned` |
| `ordering` | string | Sort: `created_at`, `updated_at` |
| `include_inactive` | string | Include soft-deleted |

**Response:** `200 OK`
```json
{
  "count": 1,
  "results": [
    {
      "id": "uuid",
      "policy": "uuid",
      "driver": {
        "id": "uuid",
        "client": {...},
        "first_name": "John",
        "middle_name": "Robert",
        "last_name": "Doe",
        "date_of_birth": "1985-03-15",
        "license_number": "D1234567",
        "license_state": "TX",
        "license_class": {...},
        "issue_date": "2020-01-15",
        "hire_date": "2022-06-01",
        "violations": 0,
        "accidents": 1,
        "is_active": true,
        "created_at": "...",
        "updated_at": "..."
      },
      "status": "active",
      "is_active": true,
      "created_at": "...",
      "updated_at": "..."
    }
  ]
}
```

### Create Policy Driver
```
POST /api/v1/assets/policy-drivers/
```

**Request Body:**
```json
{
  "policy_id": "uuid",
  "driver_id": "uuid",
  "status": "active"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `policy_id` | uuid | Yes | Policy ID |
| `driver_id` | uuid | Yes | Driver ID |
| `status` | string | No | Status (default: `active`) |

**Status Values:**
- `active` - Currently on policy
- `inactive` - Removed from policy
- `not_assigned` - Not yet assigned

**Error:** Returns `400` if driver already assigned to policy.

**Response:** `201 Created`

---

### Update Policy Driver
```
PUT /api/v1/assets/policy-drivers/{id}/
PATCH /api/v1/assets/policy-drivers/{id}/
```

Update status. Cannot change policy or driver assignment.

**Request Body (PATCH):**
```json
{
  "status": "inactive"
}
```

**Updatable Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `active`, `inactive`, or `not_assigned` |

**Response:** `200 OK`

---

### Remove Policy Driver (Soft Delete)
```
DELETE /api/v1/assets/policy-drivers/{id}/
```

Soft deletes the assignment (sets `is_active = false`).

**Response:** `204 No Content`

**To view removed assignments:**
```
GET /api/v1/assets/policy-drivers/?include_inactive=true
```

---

## Loss Payees

### List Loss Payees
```
GET /api/v1/assets/loss-payees/
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `search` | string | Search name, contact person name |
| `ordering` | string | Sort: `name`, `created_at` |
| `include_inactive` | string | Include soft-deleted |

**Response:** `200 OK`
```json
{
  "count": 1,
  "results": [
    {
      "id": "uuid",
      "name": "Bank of America",
      "email": "leasing@boa.com",
      "contact_person_name": "Jane Smith",
      "telephone": "800-555-1234",
      "fax": "800-555-1235",
      "cell_phone": "",
      "preference": "EMAIL",
      "remarks": "Preferred contact method is email",
      "address": {
        "id": "uuid",
        "street_address": "100 Bank St",
        "city": "Charlotte",
        "state": "NC",
        "zip_code": "28255"
      },
      "is_active": true,
      "created_at": "...",
      "updated_at": "..."
    }
  ]
}
```

### Create Loss Payee
```
POST /api/v1/assets/loss-payees/
```

**Request Body:**
```json
{
  "name": "Bank of America",
  "email": "leasing@boa.com",
  "contact_person_name": "Jane Smith",
  "telephone": "800-555-1234",
  "fax": "800-555-1235",
  "cell_phone": "",
  "preference": "EMAIL",
  "remarks": "Preferred contact method is email",
  "address": {
    "street_address": "100 Bank St",
    "city": "Charlotte",
    "state": "NC",
    "zip_code": "28255"
  }
}
```

**Required Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Loss payee name (max 255 chars) |
| `address` | object | Address details (required) |
| `address.street_address` | string | Street address |
| `address.city` | string | City |
| `address.state` | string | 2-letter state code |
| `address.zip_code` | string | ZIP code |

**Optional Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `email` | string | Email address |
| `contact_person_name` | string | Contact person (max 255 chars) |
| `telephone` | string | Phone number (max 32 chars) |
| `fax` | string | Fax number (max 32 chars) |
| `cell_phone` | string | Cell phone (max 32 chars) |
| `preference` | string | Contact preference: `EMAIL` or `FAX` |
| `remarks` | string | Additional notes |

**Response:** `201 Created`

---

## Required Lookups

| Lookup | Endpoint |
|--------|----------|
| Vehicle Types | `GET /api/v1/lookups/vehicle-types/` |
| License Classes | `GET /api/v1/lookups/license-classes/` |

---

## Enumerations

### Policy Vehicle Status
- `active` - Vehicle currently on policy
- `inactive` - Vehicle removed from policy
- `unassigned` - Vehicle not yet assigned

### Policy Driver Status
- `active` - Driver currently on policy
- `inactive` - Driver removed from policy
- `not_assigned` - Driver not yet assigned

### Loss Payee Preference
- `EMAIL` - Contact via email
- `FAX` - Contact via fax

---

## VIN Validation

VINs must be exactly 17 characters and exclude letters I, O, and Q.

**Valid:** `1HGCM82633A123456`
**Invalid:** `1HGOM82633A12345` (contains O, only 16 chars)

---

## Notes

- VIN must be globally unique across all vehicles
- Client + license_number must be unique for drivers
- Policy + vehicle must be unique for policy-vehicles
- Policy + driver must be unique for policy-drivers
- Garaging address must be an existing Address record

