# Timeline / Activity Log API Documentation

## Overview

The Activity Log API provides a complete history of all actions performed within the system. This powers the "Timeline" page showing everything that happened to a client/account.

**Base URL:** `/api/v1/activity-logs/`

**Authentication:** All endpoints require JWT Bearer token authentication.

---

## List Activity Logs

```
GET /api/v1/activity-logs/
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `client` | uuid | **Filter by client ID** - Show all actions for a specific client |
| `policy` | uuid | Filter by policy ID |
| `endorsement` | uuid | Filter by endorsement ID |
| `action_type` | string | Filter by action type (see Action Types below) |
| `action_type__in` | string | Filter by multiple action types (comma-separated) |
| `performed_by` | uuid | Filter by user who performed the action |
| `timestamp` | datetime | Exact timestamp |
| `timestamp__gte` | datetime | Timestamp on or after |
| `timestamp__lte` | datetime | Timestamp on or before |
| `timestamp__date` | date | Filter by date only |
| `search` | string | Search transaction name, description, notes, policy number, client name, VIN, driver name |
| `ordering` | string | Sort: `timestamp`, `-timestamp`, `action_type`, `transaction_name` |
| `page` | integer | Page number |

**Response:** `200 OK`
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "action_type": "vehicle_assigned",
      "action_type_display": "Assign Vehicle",
      "transaction_name": "Vehicle Assigned: 4V4NC912GLR321551",
      "description": "Truck VIN 4V4NC912GLR321551 was assigned to policy Trinity / Lloyd's, Policy Number 238394-001APD-93755 on 09/24/2025 09:37:46 AM by Amir Mambetaliev",
      "notes": "",
      "timestamp": "2025-09-24T09:37:46Z",
      "client": "uuid",
      "policy": "uuid",
      "endorsement": null,
      "vehicle": "uuid",
      "driver": null,
      "client_name": "Acme Logistics",
      "carrier_name": "Trinity / Lloyd's",
      "policy_number": "238394-001APD-93755",
      "vehicle_info": {
        "id": "uuid",
        "vin": "4V4NC912GLR321551",
        "unit_number": "TRUCK-001",
        "year": 2023,
        "make": "Volvo",
        "model": "VNL"
      },
      "driver_info": null,
      "endorsement_name": null,
      "performed_by": {
        "id": "uuid",
        "email": "amir@example.com",
        "first_name": "Amir",
        "last_name": "Mambetaliev",
        "full_name": "Amir Mambetaliev"
      },
      "metadata": {}
    },
    {
      "id": "uuid",
      "action_type": "endorsement_completed",
      "action_type_display": "Endorsement Completed",
      "transaction_name": "Endorsement Completed: Endorsement 09/17/2025",
      "description": "Endorsement 'Endorsement 09/17/2025' was completed on 09/17/2025 02:30:00 PM by Sarah Jones",
      "notes": "",
      "timestamp": "2025-09-17T14:30:00Z",
      "client": "uuid",
      "policy": "uuid",
      "endorsement": "uuid",
      "vehicle": null,
      "driver": null,
      "client_name": "Acme Logistics",
      "carrier_name": "Great Insurance Co",
      "policy_number": "POL-2025-001",
      "vehicle_info": null,
      "driver_info": null,
      "endorsement_name": "Endorsement 09/17/2025",
      "performed_by": {
        "id": "uuid",
        "email": "sarah@example.com",
        "first_name": "Sarah",
        "last_name": "Jones",
        "full_name": "Sarah Jones"
      },
      "metadata": {}
    },
    {
      "id": "uuid",
      "action_type": "policy_created",
      "action_type_display": "Policy Created",
      "transaction_name": "Policy Created: POL-2025-001",
      "description": "Policy POL-2025-001 (Great Insurance Co) was created on 01/15/2025 10:00:00 AM by John Smith",
      "notes": "",
      "timestamp": "2025-01-15T10:00:00Z",
      "client": "uuid",
      "policy": "uuid",
      "endorsement": null,
      "vehicle": null,
      "driver": null,
      "client_name": "Acme Logistics",
      "carrier_name": "Great Insurance Co",
      "policy_number": "POL-2025-001",
      "vehicle_info": null,
      "driver_info": null,
      "endorsement_name": null,
      "performed_by": {
        "id": "uuid",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Smith",
        "full_name": "John Smith"
      },
      "metadata": {}
    }
  ]
}
```

---

## Retrieve Activity Log Entry

```
GET /api/v1/activity-logs/{id}/
```

**Response:** `200 OK` - Same structure as list item

---

## Create Activity Log Entry

```
POST /api/v1/activity-logs/
```

**Request Body:**
```json
{
  "action_type": "user_action",
  "transaction_name": "Viewed Policy Details",
  "description": "User viewed policy POL-2025-001 details",
  "notes": "",
  "client": "uuid",
  "policy": "uuid",
  "metadata": {
    "page": "policy_details",
    "duration_seconds": 45
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action_type` | string | Yes | Action type (see below) |
| `transaction_name` | string | Yes | Display name for the action |
| `description` | string | No | Auto-generated or custom description |
| `notes` | string | No | Optional user notes |
| `client` | uuid | No | Related client ID |
| `policy` | uuid | No | Related policy ID |
| `endorsement` | uuid | No | Related endorsement ID |
| `vehicle` | uuid | No | Related vehicle ID |
| `driver` | uuid | No | Related driver ID |
| `metadata` | object | No | Additional JSON data |

**Note:** `performed_by` is automatically set to the authenticated user.

**Response:** `201 Created`

---

## Action Types

### Client Actions
| Value | Display Name | Description |
|-------|--------------|-------------|
| `client_created` | Client Created | New client was created |
| `client_updated` | Client Updated | Client information was modified |

### Policy Actions
| Value | Display Name | Description |
|-------|--------------|-------------|
| `policy_created` | Policy Created | New policy was created |
| `policy_updated` | Policy Updated | Policy was modified |
| `policy_bound` | Policy Bound | Policy was bound |
| `policy_cancelled` | Policy Cancelled | Policy was cancelled |

### Vehicle Actions
| Value | Display Name | Description |
|-------|--------------|-------------|
| `vehicle_created` | New Vehicle | New vehicle was added |
| `vehicle_updated` | Edit Vehicle | Vehicle was modified |
| `vehicle_assigned` | Assign Vehicle | Vehicle assigned to policy |
| `vehicle_removed` | Remove Vehicle | Vehicle removed from policy |

### Driver Actions
| Value | Display Name | Description |
|-------|--------------|-------------|
| `driver_created` | New Driver | New driver was added |
| `driver_updated` | Edit Driver | Driver was modified |
| `driver_assigned` | Assign Driver | Driver assigned to policy |
| `driver_removed` | Remove Driver | Driver removed from policy |

### Endorsement Actions
| Value | Display Name | Description |
|-------|--------------|-------------|
| `endorsement_created` | Endorsement Created | Endorsement was started |
| `endorsement_started` | Endorsement Started | Endorsement processing began |
| `endorsement_completed` | Endorsement Completed | Endorsement was finalized |
| `endorsement_cancelled` | Endorsement Cancelled | Endorsement was cancelled |
| `endorsement_updated` | Endorsement Updated | Endorsement was modified |

### Certificate Actions
| Value | Display Name | Description |
|-------|--------------|-------------|
| `certificate_created` | Certificate Created | Certificate was generated |
| `certificate_updated` | Certificate Updated | Certificate was regenerated |

### General
| Value | Display Name | Description |
|-------|--------------|-------------|
| `user_action` | User Action | Generic user action (page views, etc.) |

---

## Common Use Cases

### Get all activity for a client (Timeline page)

```
GET /api/v1/activity-logs/?client={client_id}&ordering=-timestamp
```

### Filter by action type

```
GET /api/v1/activity-logs/?action_type=vehicle_assigned
GET /api/v1/activity-logs/?action_type__in=vehicle_assigned,driver_assigned
```

### Filter by date range

```
GET /api/v1/activity-logs/?timestamp__gte=2025-01-01&timestamp__lte=2025-12-31
```

### Filter by carrier/policy

```
GET /api/v1/activity-logs/?policy={policy_id}
```

### Sort by different columns

```
GET /api/v1/activity-logs/?ordering=timestamp        # Oldest first
GET /api/v1/activity-logs/?ordering=-timestamp       # Newest first (default)
GET /api/v1/activity-logs/?ordering=action_type      # By type
GET /api/v1/activity-logs/?ordering=transaction_name # By name
```

### Search

```
GET /api/v1/activity-logs/?search=4V4NC912GLR321551  # Search by VIN
GET /api/v1/activity-logs/?search=POL-2025-001       # Search by policy number
```

---

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | uuid | Unique identifier |
| `action_type` | string | Action type code |
| `action_type_display` | string | Human-readable action type |
| `transaction_name` | string | Display name (shown in UI) |
| `description` | string | Detailed log trail message |
| `notes` | string | Optional notes |
| `timestamp` | datetime | When action occurred |
| `client` | uuid | Related client ID |
| `policy` | uuid | Related policy ID |
| `endorsement` | uuid | Related endorsement ID |
| `vehicle` | uuid | Related vehicle ID |
| `driver` | uuid | Related driver ID |
| `client_name` | string | Client company name |
| `carrier_name` | string | Insurance company name (from policy) |
| `policy_number` | string | Policy number |
| `vehicle_info` | object | Vehicle details if applicable |
| `driver_info` | object | Driver details if applicable |
| `endorsement_name` | string | Endorsement name if applicable |
| `performed_by` | object | User who performed the action |
| `metadata` | object | Additional custom data |

---

## Notes

- Activity logs are immutable - they cannot be updated or deleted via API
- The `performed_by` field is auto-populated from the authenticated user on create
- Timestamps are in ISO 8601 format (UTC)
- Use the `client` filter to get the complete timeline for a specific client
- The `description` field contains the auto-generated "log trail" message
- `carrier_name` and `policy_number` are computed from the related policy

