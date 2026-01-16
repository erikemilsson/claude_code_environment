# API Documentation Patterns

## Purpose

This guide provides specific standards and patterns for documenting REST APIs, GraphQL APIs, and other programmatic interfaces. Consistent API documentation helps developers integrate quickly and reduces support burden.

## API Documentation Principles

1. **Completeness**: Document every endpoint, parameter, and response
2. **Accuracy**: Keep docs in sync with actual API behavior
3. **Usability**: Make it easy to find and understand information
4. **Testability**: Provide runnable examples
5. **Discoverability**: Help developers find the endpoints they need

## REST API Documentation

### Endpoint Overview Page

For large APIs, create an overview page listing all endpoints grouped by resource:

```markdown
# API Reference

## Authentication
- [POST /auth/login](#post-authlogin) - Authenticate and get token
- [POST /auth/logout](#post-authlogout) - Invalidate token
- [POST /auth/refresh](#post-authrefresh) - Refresh access token

## Users
- [GET /users](#get-users) - List users
- [GET /users/{id}](#get-usersid) - Get user details
- [POST /users](#post-users) - Create user
- [PUT /users/{id}](#put-usersid) - Update user
- [DELETE /users/{id}](#delete-usersid) - Delete user

## Projects
- [GET /projects](#get-projects) - List projects
- [POST /projects](#post-projects) - Create project
...
```

### Endpoint Documentation Template

```markdown
# [HTTP METHOD] [Endpoint Path]

Brief one-sentence description.

## Endpoint
```
[METHOD] https://api.example.com/v1/resource/{id}
```

## Description
Detailed explanation of what this endpoint does, when to use it, and any important context.

## Authentication
**Required**: Yes/No
**Type**: API Key / OAuth 2.0 / JWT / Basic Auth
**Scopes**: `read:resource`, `write:resource` (if applicable)

## Rate Limiting
- **Limit**: 100 requests per minute per API key
- **Headers**:
  - `X-RateLimit-Limit`: Total allowed requests
  - `X-RateLimit-Remaining`: Requests remaining
  - `X-RateLimit-Reset`: Timestamp when limit resets

## URL Parameters

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `id` | string | Yes | Resource unique identifier | `usr_1234` |

## Query Parameters

| Parameter | Type | Required | Default | Constraints | Description |
|-----------|------|----------|---------|-------------|-------------|
| `page` | integer | No | 1 | ≥ 1 | Page number for pagination |
| `limit` | integer | No | 10 | 1-100 | Number of results per page |
| `sort` | string | No | `created_at` | Allowed: `created_at`, `updated_at`, `name` | Sort field |
| `order` | string | No | `desc` | `asc` or `desc` | Sort direction |
| `filter[status]` | string | No | - | `active`, `inactive`, `pending` | Filter by status |

## Request Headers

| Header | Required | Description | Example |
|--------|----------|-------------|---------|
| `Authorization` | Yes | Bearer token for authentication | `Bearer eyJ0eXAiOiJKV1...` |
| `Content-Type` | Yes (for POST/PUT) | Must be `application/json` | `application/json` |
| `Accept` | No | Response format | `application/json` |
| `X-Request-ID` | No | Unique request identifier for tracing | `550e8400-e29b-41d4-a716-446655440000` |

## Request Body

**Content-Type**: `application/json`

### Schema
```json
{
  "name": "string (required, 1-255 characters)",
  "email": "string (required, valid email format)",
  "role": "string (optional, one of: 'admin', 'user', 'viewer')",
  "metadata": {
    "key": "value (optional, object with string keys and values)"
  },
  "tags": ["string (optional, array of strings)"]
}
```

### Field Descriptions

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-------------|-------------|
| `name` | string | Yes | 1-255 chars | User's full name |
| `email` | string | Yes | Valid email | User's email address |
| `role` | string | No | Enum: `admin`, `user`, `viewer` | User's role in the system |
| `metadata` | object | No | Max 10 key-value pairs | Custom metadata |
| `tags` | array | No | Max 5 tags | Classification tags |

### Example Request
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "role": "user",
  "metadata": {
    "department": "Engineering",
    "team": "Platform"
  },
  "tags": ["developer", "full-time"]
}
```

## Response

### Success Response

#### 200 OK (for GET, PUT, DELETE)
```json
{
  "id": "usr_1234567890",
  "name": "Jane Doe",
  "email": "jane@example.com",
  "role": "user",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "metadata": {
    "department": "Engineering",
    "team": "Platform"
  },
  "tags": ["developer", "full-time"]
}
```

#### 201 Created (for POST)
```json
{
  "id": "usr_1234567890",
  "name": "Jane Doe",
  "email": "jane@example.com",
  "role": "user",
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z",
  "metadata": {
    "department": "Engineering",
    "team": "Platform"
  },
  "tags": ["developer", "full-time"]
}
```

**Response Headers**:
- `Location: https://api.example.com/v1/users/usr_1234567890`

#### 204 No Content (for DELETE)
No response body.

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique user identifier |
| `name` | string | User's full name |
| `email` | string | User's email address |
| `role` | string | User's role (`admin`, `user`, `viewer`) |
| `status` | string | Account status (`active`, `inactive`, `pending`) |
| `created_at` | string (ISO 8601) | When the user was created |
| `updated_at` | string (ISO 8601) | When the user was last updated |
| `metadata` | object | Custom metadata |
| `tags` | array | Classification tags |

### Error Responses

#### 400 Bad Request
**Cause**: Invalid input, validation errors

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "issue": "Invalid email format",
        "value": "not-an-email"
      },
      {
        "field": "role",
        "issue": "Invalid value. Must be one of: admin, user, viewer",
        "value": "superuser"
      }
    ]
  },
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### 401 Unauthorized
**Cause**: Missing or invalid authentication

```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Authentication required. Please provide a valid API token."
  },
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### 403 Forbidden
**Cause**: Authenticated but lacking permissions

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "You don't have permission to perform this action",
    "required_scope": "write:users"
  },
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### 404 Not Found
**Cause**: Resource doesn't exist

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "User not found",
    "resource_id": "usr_nonexistent"
  },
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### 409 Conflict
**Cause**: Resource conflict (e.g., duplicate email)

```json
{
  "error": {
    "code": "CONFLICT",
    "message": "A user with this email already exists",
    "conflicting_field": "email",
    "conflicting_value": "jane@example.com"
  },
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### 422 Unprocessable Entity
**Cause**: Semantically invalid request

```json
{
  "error": {
    "code": "UNPROCESSABLE",
    "message": "Cannot assign admin role to inactive user"
  },
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### 429 Too Many Requests
**Cause**: Rate limit exceeded

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later.",
    "retry_after": 60
  },
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response Headers**:
- `Retry-After: 60` (seconds until limit resets)

#### 500 Internal Server Error
**Cause**: Server-side error

```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An internal error occurred. Please try again later.",
    "support": "Contact support@example.com with request ID"
  },
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

#### 503 Service Unavailable
**Cause**: Service temporarily unavailable (maintenance, overload)

```json
{
  "error": {
    "code": "SERVICE_UNAVAILABLE",
    "message": "Service temporarily unavailable",
    "retry_after": 300
  },
  "request_id": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response Headers**:
- `Retry-After: 300`

## Code Examples

### cURL
```bash
curl -X POST https://api.example.com/v1/users \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "role": "user"
  }'
```

### Python (requests)
```python
import requests

url = "https://api.example.com/v1/users"
headers = {
    "Authorization": "Bearer YOUR_API_TOKEN",
    "Content-Type": "application/json"
}
data = {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "role": "user"
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 201:
    user = response.json()
    print(f"Created user: {user['id']}")
else:
    error = response.json()
    print(f"Error: {error['error']['message']}")
```

### JavaScript (fetch)
```javascript
const createUser = async () => {
  try {
    const response = await fetch('https://api.example.com/v1/users', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer YOUR_API_TOKEN',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: 'Jane Doe',
        email: 'jane@example.com',
        role: 'user'
      })
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error.message);
    }

    const user = await response.json();
    console.log('Created user:', user.id);
    return user;
  } catch (error) {
    console.error('Error creating user:', error.message);
  }
};
```

### Node.js (axios)
```javascript
const axios = require('axios');

const createUser = async () => {
  try {
    const response = await axios.post(
      'https://api.example.com/v1/users',
      {
        name: 'Jane Doe',
        email: 'jane@example.com',
        role: 'user'
      },
      {
        headers: {
          'Authorization': 'Bearer YOUR_API_TOKEN',
          'Content-Type': 'application/json'
        }
      }
    );

    console.log('Created user:', response.data.id);
    return response.data;
  } catch (error) {
    if (error.response) {
      console.error('Error:', error.response.data.error.message);
    } else {
      console.error('Error:', error.message);
    }
  }
};
```

### Ruby
```ruby
require 'net/http'
require 'json'

uri = URI('https://api.example.com/v1/users')
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true

request = Net::HTTP::Post.new(uri.path)
request['Authorization'] = 'Bearer YOUR_API_TOKEN'
request['Content-Type'] = 'application/json'
request.body = {
  name: 'Jane Doe',
  email: 'jane@example.com',
  role: 'user'
}.to_json

response = http.request(request)

if response.code == '201'
  user = JSON.parse(response.body)
  puts "Created user: #{user['id']}"
else
  error = JSON.parse(response.body)
  puts "Error: #{error['error']['message']}"
end
```

## Notes
Additional context, best practices, or important warnings.

## Related Endpoints
- [GET /users/{id}](#get-usersid) - Retrieve this user
- [PUT /users/{id}](#put-usersid) - Update this user
- [DELETE /users/{id}](#delete-usersid) - Delete this user

## Changelog
- **v1.2** (2024-02-01): Added `tags` field
- **v1.1** (2024-01-15): Added `metadata` support
- **v1.0** (2023-12-01): Initial release
```

## Pagination Pattern

For endpoints returning lists:

```markdown
## Pagination

This endpoint supports cursor-based pagination.

### Query Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | 10 | Items per page (max 100) |
| `cursor` | string | - | Pagination cursor from previous response |

### Response Structure

```json
{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6MTIzNH0=",
    "has_more": true,
    "total_count": 150
  }
}
```

### Example: Paginating Through Results

```python
def get_all_users(api_token):
    users = []
    cursor = None

    while True:
        params = {'limit': 100}
        if cursor:
            params['cursor'] = cursor

        response = requests.get(
            'https://api.example.com/v1/users',
            headers={'Authorization': f'Bearer {api_token}'},
            params=params
        )

        data = response.json()
        users.extend(data['data'])

        if not data['pagination']['has_more']:
            break

        cursor = data['pagination']['next_cursor']

    return users
```
```

## Filtering and Sorting Pattern

```markdown
## Filtering

Use query parameters with `filter[field]` syntax:

```
GET /users?filter[status]=active&filter[role]=admin
```

### Supported Filters

| Filter | Type | Values | Description |
|--------|------|--------|-------------|
| `filter[status]` | string | `active`, `inactive`, `pending` | Filter by account status |
| `filter[role]` | string | `admin`, `user`, `viewer` | Filter by role |
| `filter[created_after]` | string (ISO 8601) | Any valid date | Users created after this date |
| `filter[created_before]` | string (ISO 8601) | Any valid date | Users created before this date |

### Combining Filters

Multiple filters use AND logic:

```
GET /users?filter[status]=active&filter[role]=admin
```

Returns: Active users who are also admins.

## Sorting

Use `sort` and `order` parameters:

```
GET /users?sort=created_at&order=desc
```

### Supported Sort Fields

| Field | Description |
|-------|-------------|
| `created_at` | Sort by creation date (default) |
| `updated_at` | Sort by last update |
| `name` | Sort alphabetically by name |
| `email` | Sort alphabetically by email |

### Sort Order

- `asc` - Ascending (A-Z, oldest first)
- `desc` - Descending (Z-A, newest first) (default)
```

## Webhooks Documentation Pattern

```markdown
# Webhooks

## Overview

Webhooks allow you to receive real-time notifications when events occur in your account.

## Setup

### 1. Create Webhook Endpoint

Create an HTTPS endpoint in your application that can receive POST requests.

### 2. Register Webhook URL

```bash
curl -X POST https://api.example.com/v1/webhooks \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://yourapp.com/webhooks",
    "events": ["user.created", "user.updated"],
    "active": true
  }'
```

## Event Types

| Event | Description | Payload |
|-------|-------------|---------|
| `user.created` | New user created | User object |
| `user.updated` | User updated | User object |
| `user.deleted` | User deleted | User ID |

## Webhook Payload

```json
{
  "id": "evt_1234567890",
  "type": "user.created",
  "created_at": "2024-01-15T10:30:00Z",
  "data": {
    "id": "usr_1234567890",
    "name": "Jane Doe",
    "email": "jane@example.com",
    ...
  }
}
```

## Signature Verification

Verify webhook signatures to ensure requests are from our servers:

```python
import hmac
import hashlib

def verify_webhook_signature(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature)

# In your webhook handler
signature = request.headers.get('X-Webhook-Signature')
if not verify_webhook_signature(request.body, signature, WEBHOOK_SECRET):
    return 401  # Unauthorized
```

## Retry Logic

- Failed webhooks are retried 3 times with exponential backoff
- Timeouts occur after 10 seconds
- Your endpoint should return 2xx status code to acknowledge receipt

## Best Practices

1. **Respond Quickly**: Return 200 OK immediately, process asynchronously
2. **Verify Signatures**: Always verify webhook signatures
3. **Handle Duplicates**: Use event IDs to detect and ignore duplicates
4. **Implement Retry Logic**: Handle temporary failures gracefully
```

## API Changelog Pattern

```markdown
# API Changelog

## Versioning Policy

- **Major version** (v1 → v2): Breaking changes
- **Minor updates**: New features, backwards-compatible
- **Patches**: Bug fixes, documentation updates

Current version: **v1**

## v1.3.0 (2024-02-15)

### Added
- New endpoint: `GET /users/{id}/activity`
- Support for filtering users by multiple tags
- Pagination now includes `total_count` field

### Changed
- Increased rate limit to 150 requests per minute
- `created_at` and `updated_at` now include milliseconds

### Deprecated
- `GET /users/list` - Use `GET /users` instead
- Will be removed in v2.0

### Fixed
- Pagination cursor encoding for non-ASCII characters
- 404 error message clarity

## v1.2.0 (2024-01-15)

...
```

## Best Practices

### 1. Consistent Structure

Use the same structure for all endpoint documentation:
- Endpoint and method
- Description
- Authentication
- Parameters
- Request/response examples
- Error responses
- Code examples

### 2. Complete Examples

Provide working code examples that developers can copy and paste:
- Show authentication
- Include all required parameters
- Handle common errors
- Use realistic data

### 3. Error Documentation

Document all possible error responses:
- HTTP status codes
- Error codes/types
- Error messages
- Resolution steps

### 4. Keep in Sync

API docs must match actual API behavior:
- Generate docs from code when possible
- Test all examples with CI/CD
- Version documentation with API versions
- Update immediately when API changes

### 5. Interactive Documentation

Consider tools for interactive API docs:
- Swagger/OpenAPI
- Postman collections
- Interactive code playgrounds
- "Try it" features

### 6. Search and Navigation

Make it easy to find information:
- Searchable documentation
- Group endpoints by resource
- Clear table of contents
- Quick reference pages

### 7. Authentication Documentation

Create separate authentication guide:
- How to get API keys
- Token refresh flows
- Security best practices
- Scopes and permissions

### 8. Rate Limiting

Document rate limits clearly:
- Limits per endpoint or global
- How limits are calculated
- Response headers
- How to handle 429 errors

## Tools and Automation

### Documentation Generators

- **Swagger/OpenAPI**: Generate docs from OpenAPI spec
- **Redoc**: Beautiful API docs from OpenAPI
- **Slate**: Static API documentation
- **Stoplight**: API design and documentation platform

### Testing Documentation

- **Dredd**: Test API responses against documentation
- **Postman**: Create and test API collections
- **Paw/Insomnia**: API clients for testing

### Keeping Docs Current

- Generate from code annotations/decorators
- Run tests against documented examples
- Auto-update changelog from git commits
- Version docs alongside API code
