# Garaging Addresses API Guide

This document provides detailed information about all endpoints related to garaging addresses in the IMS system.

## Overview

Garaging addresses represent the physical location where a vehicle is primarily stored/garaged. They can be:
1. **Attached directly to a Vehicle** - Default garaging location for the vehicle
2. **Attached via PolicyVehicle** - Policy-specific garaging location (can differ per policy)

---

## Client Garaging Addresses

### Get All Garaging Addresses for a Client

Retrieves all garaging addresses associated with a client's vehicles (both direct and policy-assigned).

```http
GET /api/v1/clients/{client_id}/garaging-addresses/
Authorization: Bearer <token>
```

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `client_id` | UUID | Client ID |

**Response (200 OK):**

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "street_address": "123 Main Street",
    "city": "Dallas",
    "state": "TX",
    "zip_code": "75201"
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "street_address": "456 Oak Avenue",
    "city": "Houston",
    "state": "TX",
    "zip_code": "77001"
  }
]
```

This endpoint returns a deduplicated list of all addresses from:
- Addresses directly attached to the client's vehicles (`garaging_address`)
- Addresses from policy vehicle assignments (`PolicyVehicle.garaging_address`)

---

## Address Endpoints

Base path: `/api/v1/addresses/`

### List Addresses

```http
GET /api/v1/addresses/
Authorization: Bearer <token>
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `search` | string | Search in street_address, city, state, zip_code |
| `ordering` | string | Sort by field. Options: `street_address`, `city`, `state`, `created_at`. Prefix with `-` for descending. Default: `street_address` |
| `include_inactive` | boolean | Include soft-deleted addresses. Values: `true`, `1`, `yes` |
| `page` | integer | Page number for pagination |

**Response:**

```json
{
  "count": 25,
  "next": "http://localhost:8000/api/v1/addresses/?page=2",
  "previous": null,
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "street_address": "123 Main Street",
      "city": "Dallas",
      "state": "TX",
      "zip_code": "75201"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "street_address": "456 Oak Avenue",
      "city": "Houston",
      "state": "TX",
      "zip_code": "77001"
    }
  ]
}
```

---

### Create Address

```http
POST /api/v1/addresses/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**

```json
{
  "street_address": "123 Main Street",
  "city": "Dallas",
  "state": "TX",
  "zip_code": "75201"
}
```

**Field Specifications:**

| Field | Type | Required | Max Length | Description |
|-------|------|----------|------------|-------------|
| `street_address` | string | Yes | 255 | Street address line |
| `city` | string | Yes | 128 | City name |
| `state` | string | Yes | 2 | Two-letter state code (e.g., TX, CA) |
| `zip_code` | string | Yes | 10 | ZIP code (supports ZIP+4 format) |

**Response (201 Created):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "street_address": "123 Main Street",
  "city": "Dallas",
  "state": "TX",
  "zip_code": "75201"
}
```

**Error Response (400 Bad Request):**

```json
{
  "street_address": ["This field is required."],
  "state": ["Ensure this field has no more than 2 characters."]
}
```

---

### Retrieve Address

```http
GET /api/v1/addresses/{id}/
Authorization: Bearer <token>
```

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | UUID | Address ID |

**Response (200 OK):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "street_address": "123 Main Street",
  "city": "Dallas",
  "state": "TX",
  "zip_code": "75201"
}
```

**Error Response (404 Not Found):**

```json
{
  "detail": "No Address matches the given query."
}
```

---

### Update Address (Full)

```http
PUT /api/v1/addresses/{id}/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**

```json
{
  "street_address": "789 Updated Boulevard",
  "city": "Austin",
  "state": "TX",
  "zip_code": "78701"
}
```

**Response (200 OK):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "street_address": "789 Updated Boulevard",
  "city": "Austin",
  "state": "TX",
  "zip_code": "78701"
}
```

---

### Update Address (Partial)

```http
PATCH /api/v1/addresses/{id}/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**

```json
{
  "zip_code": "78702"
}
```

**Response (200 OK):**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "street_address": "789 Updated Boulevard",
  "city": "Austin",
  "state": "TX",
  "zip_code": "78702"
}
```

---

### Delete Address (Soft Delete)

```http
DELETE /api/v1/addresses/{id}/
Authorization: Bearer <token>
```

**Response (204 No Content):**

No response body. The address is soft-deleted (marked as `is_active=false`).

---

## Vehicle Garaging Address

Vehicles can have a default garaging address attached directly. You can either:
1. Pass an existing `garaging_address_id`
2. Pass a `new_garaging_address` object to create a new address

### Create Vehicle with Existing Address ID

```http
POST /api/v1/assets/vehicles/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**

```json
{
  "client_id": "client-uuid-here",
  "vin": "1HGCM82633A123456",
  "unit_number": "TRUCK-001",
  "vehicle_type_id": "vehicle-type-uuid",
  "year": 2023,
  "make": "Freightliner",
  "model": "Cascadia",
  "gvw": 80000,
  "pd_amount": "125000.00",
  "deductible": "2500.00",
  "loss_payee_id": "loss-payee-uuid",
  "garaging_address_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

### Create Vehicle with New Address (Inline)

If you don't have an existing address ID, you can create a new address inline:

```http
POST /api/v1/assets/vehicles/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**

```json
{
  "client_id": "client-uuid-here",
  "vin": "1HGCM82633A123456",
  "unit_number": "TRUCK-001",
  "vehicle_type_id": "vehicle-type-uuid",
  "year": 2023,
  "make": "Freightliner",
  "model": "Cascadia",
  "gvw": 80000,
  "pd_amount": "125000.00",
  "deductible": "2500.00",
  "new_garaging_address": {
    "street_address": "123 Main Street",
    "city": "Dallas",
    "state": "TX",
    "zip_code": "75201"
  }
}
```

**Note:** If both `garaging_address_id` and `new_garaging_address` are provided, `garaging_address_id` takes precedence.

**Response (201 Created):**

```json
{
  "id": "vehicle-uuid",
  "client": {
    "id": "client-uuid-here",
    "company_name": "Acme Trucking"
  },
  "vin": "1HGCM82633A123456",
  "unit_number": "TRUCK-001",
  "vehicle_type": {
    "id": "vehicle-type-uuid",
    "name": "Tractor",
    "description": "Semi-truck tractor unit"
  },
  "year": 2023,
  "make": "Freightliner",
  "model": "Cascadia",
  "gvw": 80000,
  "pd_amount": "125000.00",
  "deductible": "2500.00",
  "loss_payee": {
    "id": "loss-payee-uuid",
    "name": "First National Bank",
    "address": { ... }
  },
  "garaging_address": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "street_address": "123 Main Street",
    "city": "Dallas",
    "state": "TX",
    "zip_code": "75201"
  },
  "garaging_addresses": [],
  "is_active": true,
  "created_at": "2025-11-28T10:30:00Z",
  "updated_at": "2025-11-28T10:30:00Z"
}
```

### Update Vehicle Garaging Address

```http
PATCH /api/v1/assets/vehicles/{id}/
Authorization: Bearer <token>
Content-Type: application/json
```

**Option 1: Use existing address ID:**

```json
{
  "garaging_address_id": "new-address-uuid"
}
```

**Option 2: Create new address inline:**

```json
{
  "new_garaging_address": {
    "street_address": "789 New Location",
    "city": "Austin",
    "state": "TX",
    "zip_code": "78701"
  }
}
```

**To remove the garaging address:**

```json
{
  "garaging_address_id": null
}
```

---

## Policy Vehicle Garaging Address

When assigning a vehicle to a policy, you can specify a policy-specific garaging address.

### Create Policy Vehicle Assignment

```http
POST /api/v1/assets/policy-vehicles/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**

```json
{
  "policy_id": "policy-uuid",
  "vehicle_id": "vehicle-uuid",
  "garaging_address_id": "address-uuid",
  "status": "active",
  "inception_date": "2025-01-01",
  "termination_date": null
}
```

**Field Specifications:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `policy_id` | UUID | Yes | The policy to assign the vehicle to |
| `vehicle_id` | UUID | Yes | The vehicle being assigned |
| `garaging_address_id` | UUID | Yes | Garaging address for this policy assignment |
| `status` | string | No | `active`, `inactive`, or `unassigned`. Default: `active` |
| `inception_date` | date | No | When the vehicle was added to the policy |
| `termination_date` | date | No | When the vehicle was removed from the policy |

**Response (201 Created):**

```json
{
  "id": "policy-vehicle-uuid",
  "policy": "policy-uuid",
  "vehicle": {
    "id": "vehicle-uuid",
    "vin": "1HGCM82633A123456",
    "unit_number": "TRUCK-001",
    "make": "Freightliner",
    "model": "Cascadia",
    ...
  },
  "garaging_address": {
    "id": "address-uuid",
    "street_address": "123 Main Street",
    "city": "Dallas",
    "state": "TX",
    "zip_code": "75201"
  },
  "status": "active",
  "inception_date": "2025-01-01",
  "termination_date": null,
  "is_active": true,
  "created_at": "2025-11-28T10:30:00Z",
  "updated_at": "2025-11-28T10:30:00Z"
}
```

### Update Policy Vehicle Garaging Address

```http
PATCH /api/v1/assets/policy-vehicles/{id}/
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body:**

```json
{
  "garaging_address_id": "new-address-uuid"
}
```

---

## Vehicle Response with All Garaging Addresses

When retrieving a vehicle, the response includes both types of garaging addresses:

```http
GET /api/v1/assets/vehicles/{id}/
Authorization: Bearer <token>
```

**Response:**

```json
{
  "id": "vehicle-uuid",
  "vin": "1HGCM82633A123456",
  "unit_number": "TRUCK-001",
  ...
  "garaging_address": {
    "id": "address-uuid-1",
    "street_address": "123 Main Street",
    "city": "Dallas",
    "state": "TX",
    "zip_code": "75201"
  },
  "garaging_addresses": [
    {
      "policy_id": "policy-uuid-1",
      "policy_number": "POL-2025-001",
      "status": "active",
      "address": {
        "id": "address-uuid-2",
        "street_address": "456 Oak Avenue",
        "city": "Houston",
        "state": "TX",
        "zip_code": "77001"
      }
    },
    {
      "policy_id": "policy-uuid-2",
      "policy_number": "POL-2025-002",
      "status": "active",
      "address": {
        "id": "address-uuid-3",
        "street_address": "789 Pine Road",
        "city": "Austin",
        "state": "TX",
        "zip_code": "78701"
      }
    }
  ]
}
```

**Field Descriptions:**

| Field | Description |
|-------|-------------|
| `garaging_address` | Default garaging address attached directly to the vehicle |
| `garaging_addresses` | Array of policy-specific garaging addresses from active PolicyVehicle assignments |

---

## Complete Workflow Example

### Step 1: Create a Garaging Address

```http
POST /api/v1/addresses/
Content-Type: application/json

{
  "street_address": "500 Industrial Blvd",
  "city": "Fort Worth",
  "state": "TX",
  "zip_code": "76101"
}
```

Response: `{ "id": "addr-123", ... }`

### Step 2: Create a Vehicle with the Address

```http
POST /api/v1/assets/vehicles/
Content-Type: application/json

{
  "client_id": "client-456",
  "vin": "1XPWD40X1ED215307",
  "unit_number": "UNIT-100",
  "vehicle_type_id": "vtype-789",
  "year": 2024,
  "make": "Peterbilt",
  "model": "579",
  "garaging_address_id": "addr-123"
}
```

### Step 3: Assign to Policy with Different Garaging Address

```http
POST /api/v1/addresses/
Content-Type: application/json

{
  "street_address": "200 Warehouse Lane",
  "city": "Arlington",
  "state": "TX",
  "zip_code": "76010"
}
```

Response: `{ "id": "addr-456", ... }`

```http
POST /api/v1/assets/policy-vehicles/
Content-Type: application/json

{
  "policy_id": "policy-001",
  "vehicle_id": "vehicle-uuid",
  "garaging_address_id": "addr-456",
  "status": "active",
  "inception_date": "2025-01-01"
}
```

Now the vehicle has:
- Default garaging address: 500 Industrial Blvd, Fort Worth
- Policy-specific garaging address: 200 Warehouse Lane, Arlington

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Created successfully |
| 204 | Deleted successfully (no content) |
| 400 | Bad request - validation error |
| 401 | Unauthorized - missing or invalid token |
| 404 | Not found - resource doesn't exist |
| 409 | Conflict - duplicate entry (e.g., policy/vehicle already assigned) |
