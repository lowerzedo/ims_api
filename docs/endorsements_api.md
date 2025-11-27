# Endorsements API Documentation

## Overview

The Endorsements API manages policy change workflows through various stages: Client → Vehicles → Drivers → Coverages → Premium → Final.

**Base URL:** `/api/v1/endorsements/`

**Authentication:** All endpoints require JWT Bearer token authentication.

---

## Endorsements

### List Endorsements
```
GET /api/v1/endorsements/
```

**Query Parameters:**
- `policy` - Filter by policy ID (exact match)
- `status` - Filter by status: `draft`, `in_progress`, `completed`, `cancelled`
- `current_stage` - Filter by stage: `client`, `vehicles`, `drivers`, `coverages`, `premium`, `final`
- `search` - Search by name, policy number, or client company name
- `ordering` - Sort by: `created_at`, `updated_at`, `effective_date` (prefix with `-` for descending)
- `include_inactive` - Include soft-deleted records: `true`, `1`, or `yes`
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 25)

**Response:** `200 OK`
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "policy": "uuid",
      "name": "Endorsement 11/26/2025",
      "status": "draft",
      "current_stage": "client",
      "effective_date": "2025-12-01",
      "premium_change": "0.00",
      "fees_change": "0.00",
      "taxes_change": "0.00",
      "agency_fee_change": "0.00",
      "total_premium_change": "0.00",
      "notes": "",
      "completed_at": null,
      "created_by": {
        "id": "uuid",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "agent"
      },
      "updated_by": {...},
      "change_types": ["Client", "Vehicles"],
      "changes": [...],
      "documents": [...],
      "created_at": "2025-11-26T10:00:00Z",
      "updated_at": "2025-11-26T10:00:00Z",
      "is_active": true
    }
  ]
}
```

---

### Create Endorsement
```
POST /api/v1/endorsements/
```

**Request Body:**
```json
{
  "policy_id": "uuid",
  "name": "Optional - auto-generated if omitted",
  "current_stage": "client",
  "effective_date": "2025-12-01",
  "premium_change": "150.00",
  "fees_change": "25.00",
  "taxes_change": "10.50",
  "agency_fee_change": "0.00",
  "total_premium_change": "185.50",
  "notes": "Added new driver"
}
```

**Required Fields:**
- `policy_id` - UUID of the policy

**Optional Fields:**
- `name` - Auto-generated as "Endorsement MM/DD/YYYY" if omitted
- `current_stage` - Defaults to `client`
- `effective_date` - Date endorsement takes effect
- `premium_change`, `fees_change`, `taxes_change`, `agency_fee_change`, `total_premium_change` - Default to `0.00`
- `notes` - Additional notes

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "policy": "uuid",
  "name": "Endorsement 12/01/2025",
  "status": "draft",
  "current_stage": "client",
  ...
}
```

---

### Retrieve Endorsement
```
GET /api/v1/endorsements/{id}/
```

**Response:** `200 OK` - Same structure as list item

---

### Update Endorsement
```
PUT /api/v1/endorsements/{id}/
PATCH /api/v1/endorsements/{id}/
```

**Request Body:** Same as create (use PATCH for partial updates)

**Read-only Fields:** `id`, `policy`, `status`, `completed_at`, `created_by`, `updated_by`, `change_types`, `changes`, `documents`, `created_at`, `updated_at`, `is_active`

**Response:** `200 OK`

---

### Delete Endorsement (Soft Delete)
```
DELETE /api/v1/endorsements/{id}/
```

Sets `is_active` to `false`. Use `?include_inactive=true` to view deleted endorsements.

**Response:** `204 No Content`

---

## Endorsement Actions

### Start Endorsement
```
POST /api/v1/endorsements/{id}/start/
```

Transitions endorsement from `draft` to `in_progress`.

**Request Body:**
```json
{
  "stage": "vehicles"  // Optional - update current stage
}
```

**Valid stages:** `client`, `vehicles`, `drivers`, `coverages`, `premium`, `final`

**Response:** `200 OK` - Returns updated endorsement

**Error:** `400 Bad Request` if endorsement is not in draft or in_progress status

---

### Advance Stage
```
POST /api/v1/endorsements/{id}/advance/
```

Move endorsement to next stage and set status to `in_progress`.

**Request Body:**
```json
{
  "stage": "premium"  // Required
}
```

**Response:** `200 OK` - Returns updated endorsement

**Error:** `400 Bad Request` if invalid stage provided

---

### Complete Endorsement
```
POST /api/v1/endorsements/{id}/complete/
```

Marks endorsement as completed, sets stage to `final`, and records completion timestamp.

**Request Body:** Empty object `{}`

**Response:** `200 OK` - Returns updated endorsement

**Error:** `400 Bad Request` if already completed

---

### Cancel Endorsement
```
POST /api/v1/endorsements/{id}/cancel/
```

Marks endorsement as cancelled and records reason in notes.

**Request Body:**
```json
{
  "reason": "Client requested cancellation"  // Optional
}
```

**Response:** `200 OK` - Returns updated endorsement

**Error:** `400 Bad Request` if already cancelled

---

## Endorsement Changes

Track granular changes within an endorsement.

### List Changes
```
GET /api/v1/endorsement-changes/
```

**Query Parameters:**
- `endorsement` - Filter by endorsement ID
- `change_type` - Filter by type: `client`, `address`, `vehicles`, `drivers`, `coverages`, `premium`, `other`
- `stage` - Filter by stage (same values as endorsement stages)
- `ordering` - Sort by: `created_at`, `updated_at`
- `include_inactive` - Include soft-deleted records

**Response:** `200 OK`
```json
{
  "count": 2,
  "results": [
    {
      "id": "uuid",
      "endorsement": "uuid",
      "stage": "vehicles",
      "change_type": "vehicles",
      "summary": "Added vehicle #1234",
      "details": {
        "vin": "1HGCM82633A123456",
        "year": 2023,
        "make": "Honda",
        "model": "Accord"
      },
      "created_by": {
        "id": "uuid",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "agent"
      },
      "created_at": "2025-11-26T10:00:00Z",
      "updated_at": "2025-11-26T10:00:00Z",
      "is_active": true
    }
  ]
}
```

---

### Create Change
```
POST /api/v1/endorsement-changes/
```

**Request Body:**
```json
{
  "endorsement_id": "uuid",
  "stage": "vehicles",
  "change_type": "vehicles",
  "summary": "Added vehicle #1234",
  "details": {
    "custom": "data",
    "can_be": "any JSON structure"
  }
}
```

**Required Fields:**
- `endorsement_id` - UUID of the endorsement
- `stage` - Stage where change occurred
- `change_type` - Type of change
- `summary` - Brief description (max 255 chars)

**Optional Fields:**
- `details` - JSON object with additional data (defaults to `{}`)

**Response:** `201 Created`

---

### Retrieve Change
```
GET /api/v1/endorsement-changes/{id}/
```

**Response:** `200 OK`

---

### Update Change
```
PUT /api/v1/endorsement-changes/{id}/
PATCH /api/v1/endorsement-changes/{id}/
```

**Request Body:** Same structure as create

**Response:** `200 OK`

---

### Delete Change (Soft Delete)
```
DELETE /api/v1/endorsement-changes/{id}/
```

**Response:** `204 No Content`

---

## Endorsement Documents

Upload and manage documents attached to endorsements.

### List Documents
```
GET /api/v1/endorsement-documents/
```

**Query Parameters:**
- `endorsement` - Filter by endorsement ID
- `stage` - Filter by stage
- `document_type` - Filter by document type ID
- `ordering` - Sort by: `created_at`, `updated_at`
- `include_inactive` - Include soft-deleted records

**Response:** `200 OK`
```json
{
  "count": 1,
  "results": [
    {
      "id": "uuid",
      "endorsement": "uuid",
      "stage": "client",
      "document_type": {
        "id": "uuid",
        "code": "LOSS_RUN",
        "name": "Loss Run",
        "description": ""
      },
      "file": "https://example.com/media/endorsements/.../document.pdf",
      "description": "Client loss run report",
      "uploaded_by": {
        "id": "uuid",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "agent"
      },
      "created_at": "2025-11-26T10:00:00Z",
      "updated_at": "2025-11-26T10:00:00Z",
      "is_active": true
    }
  ]
}
```

---

### Upload Document
```
POST /api/v1/endorsement-documents/
```

**Content-Type:** `multipart/form-data`

**Form Fields:**
- `endorsement_id` (required) - UUID of endorsement
- `file` (required) - File to upload
- `stage` (required) - Stage: `client`, `vehicles`, `drivers`, `coverages`, `premium`, `final`
- `document_type_id` (optional) - UUID of document type
- `description` (optional) - File description (max 255 chars)

**Example:**
```
POST /api/v1/endorsement-documents/
Content-Type: multipart/form-data

endorsement_id=abc-123-def-456
file=@/path/to/document.pdf
stage=client
document_type_id=doc-type-uuid
description=Client loss run report
```

**Response:** `201 Created`

---

### Retrieve Document
```
GET /api/v1/endorsement-documents/{id}/
```

**Response:** `200 OK`

---

### Update Document Metadata
```
PATCH /api/v1/endorsement-documents/{id}/
```

**Content-Type:** `multipart/form-data` (if updating file) or `application/json` (metadata only)

Update `stage`, `document_type_id`, `description`, or replace the `file`.

**Response:** `200 OK`

---

### Delete Document (Soft Delete)
```
DELETE /api/v1/endorsement-documents/{id}/
```

**Response:** `204 No Content`

---

## Enumerations

### Endorsement Status
- `draft` - Initial state
- `in_progress` - Work has started
- `completed` - Endorsement finalized
- `cancelled` - Endorsement abandoned

### Endorsement Stage
- `client` - Client information changes
- `vehicles` - Vehicle modifications
- `drivers` - Driver modifications
- `coverages` - Coverage adjustments
- `premium` - Premium calculations
- `final` - Completion/review

### Change Type
- `client` - Client information
- `address` - Address changes
- `vehicles` - Vehicle changes
- `drivers` - Driver changes
- `coverages` - Coverage changes
- `premium` - Premium adjustments
- `other` - Miscellaneous changes

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"],
  "non_field_errors": ["General error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

---

## File Storage

Documents are organized in the following structure:
```
media/endorsements/{client_id}/{policy_id}/{endorsement_id}/{filename}
```

Files are served via:
- **Local development:** `http://localhost:8000/media/...`
- **Production:** S3 or configured storage backend

---

## Notes

- All datetime fields are in ISO 8601 format with UTC timezone
- All currency fields are decimal strings with 2 decimal places
- Soft deletes preserve data - use `include_inactive=true` to view
- User fields (`created_by`, `updated_by`, `uploaded_by`) are auto-populated from authenticated user
- The `change_types` field in endorsement response is a computed array of unique change type labels

