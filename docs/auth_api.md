# Authentication & Accounts API Documentation

## Overview

The Authentication API provides JWT-based authentication and employee management for the IMS application.

**Authentication Base URL:** `/api/auth/`
**Accounts Base URL:** `/api/v1/accounts/`

**Authentication:** Token endpoints are public; all other endpoints require authentication.

---

## Obtain Token (Login)

```
POST /api/auth/token/
```

Exchange user credentials for JWT access and refresh tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | Yes | User's email address |
| `password` | string | Yes | User's password |

**Response:** `200 OK`
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

| Field | Description |
|-------|-------------|
| `access` | Short-lived access token (30 minutes) |
| `refresh` | Long-lived refresh token (7 days) |

**Error:** `401 Unauthorized`
```json
{
  "detail": "No active account found with the given credentials"
}
```

---

## Refresh Token

```
POST /api/auth/token/refresh/
```

Exchange a valid refresh token for a new access token.

**Request Body:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `refresh` | string | Yes | Valid refresh token |

**Response:** `200 OK`
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error:** `401 Unauthorized`
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

---

## Using Authentication

### Authorization Header

Include the access token in the `Authorization` header for all API requests:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Example Request

```bash
curl -X GET "https://api.example.com/api/v1/clients/" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Token Lifetimes

| Token Type | Lifetime | Use Case |
|------------|----------|----------|
| Access Token | 30 minutes | API request authentication |
| Refresh Token | 7 days | Obtaining new access tokens |

---

## Token Refresh Strategy

1. Store both tokens securely on the client
2. Use access token for API requests
3. When access token expires (401 response), use refresh token to get new access token
4. If refresh token is expired, redirect to login

### Recommended Flow

```
1. User logs in → Store access + refresh tokens
2. Make API request with access token
3. If 401 error:
   a. Call /api/auth/token/refresh/ with refresh token
   b. If successful, retry original request with new access token
   c. If refresh fails, redirect to login
4. Repeat
```

---

## User Object

When authenticated, APIs return user information in this format:

```json
{
  "id": "uuid",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "account_manager"
}
```

### User Roles

| Role | Value | Description |
|------|-------|-------------|
| Admin | `admin` | Full system access |
| Producer | `producer` | Sales/producer access |
| Account Manager | `account_manager` | Policy management access |

---

## Error Responses

### 401 Unauthorized - Invalid Credentials
```json
{
  "detail": "No active account found with the given credentials"
}
```

### 401 Unauthorized - Missing Token
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 401 Unauthorized - Invalid Token
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

### 401 Unauthorized - Expired Token
```json
{
  "detail": "Token is invalid or expired",
  "code": "token_not_valid"
}
```

---

## Security Notes

1. **Store tokens securely:**
   - Use `httpOnly` cookies or secure storage
   - Never store in localStorage for production

2. **Token transmission:**
   - Always use HTTPS
   - Don't include tokens in URLs

3. **Token rotation:**
   - Refresh tokens are NOT rotated by default
   - Access tokens should be refreshed before expiry

4. **Logout:**
   - Clear stored tokens on client
   - No server-side token invalidation (stateless JWT)

---

## JWT Payload

Access tokens contain:

```json
{
  "token_type": "access",
  "exp": 1732626000,
  "iat": 1732624200,
  "jti": "unique-token-id",
  "user_id": "uuid"
}
```

| Field | Description |
|-------|-------------|
| `token_type` | Token type (`access` or `refresh`) |
| `exp` | Expiration timestamp (Unix) |
| `iat` | Issued at timestamp (Unix) |
| `jti` | Unique token identifier |
| `user_id` | User's UUID |

---

## Configuration

| Setting | Value |
|---------|-------|
| Algorithm | HS256 |
| Access Token Lifetime | 30 minutes |
| Refresh Token Lifetime | 7 days |
| Auth Header Type | Bearer |
| Rotate Refresh Tokens | No |

---

# Employees API

Employees are users who can be assigned to policies as producers and/or account managers.

**Key Concept:** A user can be BOTH a producer AND an account manager. They may have different commission rates on different policies.

## List Employees

```
GET /api/v1/accounts/employees/
```

Returns users who can be assigned to policies.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `can_produce` | boolean | Filter users who can be producers |
| `can_manage_accounts` | boolean | Filter users who can be account managers |
| `role` | string | Filter by primary role: `producer`, `account_manager` |
| `is_active` | boolean | Filter by active status |
| `search` | string | Search email, first name, last name |
| `ordering` | string | Sort: `last_name`, `first_name`, `email`, `date_joined` |
| `include_inactive` | string | Include inactive: `true`, `1`, or `yes` |
| `page` | integer | Page number |

**Response:** `200 OK`
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": "uuid",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Smith",
      "full_name": "John Smith",
      "phone_number": "555-123-4567",
      "role": "producer",
      "can_produce": true,
      "can_manage_accounts": true,
      "default_producer_rate": "12.50",
      "default_account_manager_rate": "9.00",
      "commission_rate": "12.50",
      "is_active": true,
      "date_joined": "2024-01-15T10:00:00Z"
    },
    {
      "id": "uuid",
      "email": "sarah@example.com",
      "first_name": "Sarah",
      "last_name": "Jones",
      "full_name": "Sarah Jones",
      "phone_number": "555-987-6543",
      "role": "account_manager",
      "can_produce": false,
      "can_manage_accounts": true,
      "default_producer_rate": "0.00",
      "default_account_manager_rate": "9.50",
      "commission_rate": "0.00",
      "is_active": true,
      "date_joined": "2024-03-20T10:00:00Z"
    }
  ]
}
```

---

## Retrieve Employee

```
GET /api/v1/accounts/employees/{id}/
```

**Response:** `200 OK` - Same structure as list item

---

## Employee Capabilities

Users have capability flags that determine what roles they can be assigned on policies:

| Field | Type | Description |
|-------|------|-------------|
| `can_produce` | boolean | User can be assigned as a **producer** on policies |
| `can_manage_accounts` | boolean | User can be assigned as an **account manager** on policies |

**Note:** A user can have BOTH capabilities enabled.

---

## Commission Rates

### User-Level (Defaults)

Each user has default commission rates that apply when no policy-specific rate is set:

| Field | Description |
|-------|-------------|
| `default_producer_rate` | Default rate when assigned as producer |
| `default_account_manager_rate` | Default rate when assigned as account manager |

### Policy-Level (Overrides)

When assigning a user to a policy, you can override the default rates:

| Policy Field | Description |
|--------------|-------------|
| `producer_rate` | Rate for producer on THIS policy (overrides user default) |
| `account_manager_rate` | Rate for account manager on THIS policy (overrides user default) |

**Example:** John has a default producer rate of 12%. On Policy A, he earns 15% as producer. On Policy B, he's the account manager earning 8%.

---

## Usage Examples

### Get users who can be producers
```
GET /api/v1/accounts/employees/?can_produce=true
```

### Get users who can be account managers
```
GET /api/v1/accounts/employees/?can_manage_accounts=true
```

### Get users who can do both
```
GET /api/v1/accounts/employees/?can_produce=true&can_manage_accounts=true
```

### Search by name
```
GET /api/v1/accounts/employees/?search=smith
```

### Include inactive employees
```
GET /api/v1/accounts/employees/?include_inactive=true
```

