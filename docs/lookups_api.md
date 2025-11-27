# Lookups API Documentation

## Overview

The Lookups API provides read-only access to system reference data used across the application.

**Base URL:** `/api/v1/lookups/`

**Authentication:** No authentication required (public endpoints).

---

## Common Response Format

All lookup endpoints return the same structure:

```json
[
  {
    "id": 1,
    "name": "Lookup Value Name",
    "is_active": true
  }
]
```

**Notes:**
- Results are sorted alphabetically by `name`
- Only active (`is_active: true`) records are returned
- IDs are integers (not UUIDs)
- No pagination (all results returned)

---

## Policy Statuses

```
GET /api/v1/lookups/policy-statuses/
```

Used for: `Policy.status_id`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Active",
    "is_active": true,
    "description": "Policy is currently in force"
  },
  {
    "id": 2,
    "name": "Cancelled",
    "is_active": true,
    "description": "Policy has been cancelled"
  },
  {
    "id": 3,
    "name": "Expired",
    "is_active": true,
    "description": "Policy has reached maturity date"
  }
]
```

**Extra Field:**
- `description` - Additional details about the status

---

## Business Types

```
GET /api/v1/lookups/business-types/
```

Used for: `Policy.business_type_id`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Trucking",
    "is_active": true
  },
  {
    "id": 2,
    "name": "Passenger",
    "is_active": true
  }
]
```

---

## Insurance Types

```
GET /api/v1/lookups/insurance-types/
```

Used for: `Policy.insurance_type_id`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Commercial Auto",
    "is_active": true
  },
  {
    "id": 2,
    "name": "General Liability",
    "is_active": true
  }
]
```

---

## Policy Types

```
GET /api/v1/lookups/policy-types/
```

Used for: `Policy.policy_type_id`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "New Business",
    "is_active": true
  },
  {
    "id": 2,
    "name": "Renewal",
    "is_active": true
  }
]
```

---

## Finance Companies

```
GET /api/v1/lookups/finance-companies/
```

Used for: `Policy.finance_company_id`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Premium Finance Corp",
    "is_active": true
  },
  {
    "id": 2,
    "name": "Quick Finance LLC",
    "is_active": true
  }
]
```

---

## Contact Types

```
GET /api/v1/lookups/contact-types/
```

Used for: `Contact.contact_type_id`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Primary",
    "is_active": true
  },
  {
    "id": 2,
    "name": "Billing",
    "is_active": true
  },
  {
    "id": 3,
    "name": "Claims",
    "is_active": true
  }
]
```

---

## Address Types

```
GET /api/v1/lookups/address-types/
```

Used for: `ClientAddress.address_type_id`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Physical",
    "is_active": true
  },
  {
    "id": 2,
    "name": "Mailing",
    "is_active": true
  },
  {
    "id": 3,
    "name": "Garaging",
    "is_active": true
  }
]
```

---

## Vehicle Types

```
GET /api/v1/lookups/vehicle-types/
```

Used for: `Vehicle.vehicle_type_id`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Tractor",
    "is_active": true
  },
  {
    "id": 2,
    "name": "Trailer",
    "is_active": true
  },
  {
    "id": 3,
    "name": "Straight Truck",
    "is_active": true
  }
]
```

---

## License Classes

```
GET /api/v1/lookups/license-classes/
```

Used for: `Driver.license_class_id`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Class A CDL",
    "is_active": true
  },
  {
    "id": 2,
    "name": "Class B CDL",
    "is_active": true
  },
  {
    "id": 3,
    "name": "Class C",
    "is_active": true
  }
]
```

---

## Document Types

```
GET /api/v1/lookups/document-types/
```

Used for: `EndorsementDocument.document_type_id`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Loss Run",
    "is_active": true
  },
  {
    "id": 2,
    "name": "Driver MVR",
    "is_active": true
  },
  {
    "id": 3,
    "name": "Vehicle Schedule",
    "is_active": true
  }
]
```

---

## Quick Reference Table

| Endpoint | Used In | Field |
|----------|---------|-------|
| `/policy-statuses/` | Policy | `status_id` |
| `/business-types/` | Policy | `business_type_id` |
| `/insurance-types/` | Policy | `insurance_type_id` |
| `/policy-types/` | Policy | `policy_type_id` |
| `/finance-companies/` | Policy | `finance_company_id` |
| `/contact-types/` | Contact | `contact_type_id` |
| `/address-types/` | ClientAddress | `address_type_id` |
| `/vehicle-types/` | Vehicle | `vehicle_type_id` |
| `/license-classes/` | Driver | `license_class_id` |
| `/document-types/` | EndorsementDocument | `document_type_id` |

---

## Caching Recommendations

Since lookup data rarely changes, consider caching responses:

- **Browser cache:** Set appropriate cache headers
- **Application cache:** Store lookup data on app initialization
- **Refresh strategy:** Reload on app startup or every 24 hours

---

## Notes

- All endpoints are read-only (GET only)
- No authentication required
- Data is seeded by migrations
- IDs are stable integers
- Contact your backend team to add new lookup values

