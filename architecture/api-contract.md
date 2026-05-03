# CodePal API Contract
## Introduction
The CodePal API is a RESTful API that provides a comprehensive set of endpoints for interacting with the CodePal system. The API is designed to be used by the frontend application, as well as by third-party developers who wish to integrate CodePal into their own applications.

## Base URL and Versioning Strategy
The base URL for the CodePal API is `https://api.codepal.io/v1`. The API uses a versioning strategy, where the version number is included in the base URL. The current version of the API is `v1`.

## Authentication Scheme
The CodePal API uses a JWT Bearer token authentication scheme. All requests to the API must include a valid JWT token in the `Authorization` header. The token can be obtained by calling the `POST /api/v1/auth/login` endpoint.

## Global Error Format
All error responses from the API will be in the following format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "ERROR_MESSAGE"
  }
}
```
The `ERROR_CODE` will be a unique code that identifies the error, and the `ERROR_MESSAGE` will be a human-readable description of the error.

## Rate Limiting Policy
The CodePal API has a rate limiting policy in place to prevent abuse and ensure fair usage. The policy is as follows:

* 100 requests per minute per IP address
* 500 requests per hour per IP address
* 1000 requests per day per IP address

If the rate limit is exceeded, the API will return a `429 Too Many Requests` error response.

## Endpoints
### 1. POST /api/v1/auth/login
#### Description
Logs in a user and returns a JWT token.
#### Authentication
None
#### Request Body
```json
{
  "username": "string",
  "password": "string"
}
```
#### Success Response
```json
{
  "token": "string"
}
```
#### Error Responses
* `401 Unauthorized`: Invalid username or password
* `500 Internal Server Error`: Server error
#### Example Request/Response Pair
```bash
curl -X POST \
  https://api.codepal.io/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username": "john", "password": "password"}'
```
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

### 2. GET /api/v1/projects
#### Description
Gets a list of projects for the authenticated user.
#### Authentication
Required (JWT Bearer token)
#### Request Body
None
#### Success Response
```json
[
  {
    "id": "string",
    "name": "string",
    "description": "string"
  }
]
```
#### Error Responses
* `401 Unauthorized`: Invalid token
* `500 Internal Server Error`: Server error
#### Example Request/Response Pair
```bash
curl -X GET \
  https://api.codepal.io/v1/projects \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
```
```json
[
  {
    "id": "project-1",
    "name": "Project 1",
    "description": "This is project 1"
  },
  {
    "id": "project-2",
    "name": "Project 2",
    "description": "This is project 2"
  }
]
```

### 3. POST /api/v1/projects
#### Description
Creates a new project for the authenticated user.
#### Authentication
Required (JWT Bearer token)
#### Request Body
```json
{
  "name": "string",
  "description": "string"
}
```
#### Success Response
```json
{
  "id": "string",
  "name": "string",
  "description": "string"
}
```
#### Error Responses
* `401 Unauthorized`: Invalid token
* `400 Bad Request`: Invalid request body
* `500 Internal Server Error`: Server error
#### Example Request/Response Pair
```bash
curl -X POST \
  https://api.codepal.io/v1/projects \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' \
  -H 'Content-Type: application/json' \
  -d '{"name": "New Project", "description": "This is a new project"}'
```
```json
{
  "id": "project-3",
  "name": "New Project",
  "description": "This is a new project"
}
```

### 4. GET /api/v1/projects/{projectId}
#### Description
Gets a project by ID for the authenticated user.
#### Authentication
Required (JWT Bearer token)
#### Request Body
None
#### Success Response
```json
{
  "id": "string",
  "name": "string",
  "description": "string"
}
```
#### Error Responses
* `401 Unauthorized`: Invalid token
* `404 Not Found`: Project not found
* `500 Internal Server Error`: Server error
#### Example Request/Response Pair
```bash
curl -X GET \
  https://api.codepal.io/v1/projects/project-1 \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
```
```json
{
  "id": "project-1",
  "name": "Project 1",
  "description": "This is project 1"
}
```

### 5. PUT /api/v1/projects/{projectId}
#### Description
Updates a project by ID for the authenticated user.
#### Authentication
Required (JWT Bearer token)
#### Request Body
```json
{
  "name": "string",
  "description": "string"
}
```
#### Success Response
```json
{
  "id": "string",
  "name": "string",
  "description": "string"
}
```
#### Error Responses
* `401 Unauthorized`: Invalid token
* `404 Not Found`: Project not found
* `400 Bad Request`: Invalid request body
* `500 Internal Server Error`: Server error
#### Example Request/Response Pair
```bash
curl -X PUT \
  https://api.codepal.io/v1/projects/project-1 \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' \
  -H 'Content-Type: application/json' \
  -d '{"name": "Updated Project", "description": "This is an updated project"}'
```
```json
{
  "id": "project-1",
  "name": "Updated Project",
  "description": "This is an updated project"
}
```

### 6. DELETE /api/v1/projects/{projectId}
#### Description
Deletes a project by ID for the authenticated user.
#### Authentication
Required (JWT Bearer token)
#### Request Body
None
#### Success Response
```json
{
  "message": "Project deleted successfully"
}
```
#### Error Responses
* `401 Unauthorized`: Invalid token
* `404 Not Found`: Project not found
* `500 Internal Server Error`: Server error
#### Example Request/Response Pair
```bash
curl -X DELETE \
  https://api.codepal.io/v1/projects/project-1 \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
```
```json
{
  "message": "Project deleted successfully"
}
```

### 7. POST /api/v1/projects/{projectId}/collaborators
#### Description
Adds a collaborator to a project by ID for the authenticated user.
#### Authentication
Required (JWT Bearer token)
#### Request Body
```json
{
  "email": "string"
}
```
#### Success Response
```json
{
  "message": "Collaborator added successfully"
}
```
#### Error Responses
* `401 Unauthorized`: Invalid token
* `404 Not Found`: Project not found
* `400 Bad Request`: Invalid request body
* `500 Internal Server Error`: Server error
#### Example Request/Response Pair
```bash
curl -X POST \
  https://api.codepal.io/v1/projects/project-1/collaborators \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c' \
  -H 'Content-Type: application/json' \
  -d '{"email": "john.doe@example.com"}'
```
```json
{
  "message": "Collaborator added successfully"
}
```

### 8. GET /api/v1/projects/{projectId}/collaborators
#### Description
Gets a list of collaborators for a project by ID for the authenticated user.
#### Authentication
Required (JWT Bearer token)
#### Request Body
None
#### Success Response
```json
[
  {
    "email": "string",
    "name": "string"
  }
]
```
#### Error Responses
* `401 Unauthorized`: Invalid token
* `404 Not Found`: Project not found
* `500 Internal Server Error`: Server error
#### Example Request/Response Pair
```bash
curl -X GET \
  https://api.codepal.io/v1/projects/project-1/collaborators \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
```
```json
[
  {
    "email": "john.doe@example.com",
    "name": "John Doe"
  },
  {
    "email": "jane.doe@example.com",
    "name": "Jane Doe"
  }
]
```

### 9. DELETE /api/v1/projects/{projectId}/collaborators/{collaboratorId}
#### Description
Removes a collaborator from a project by ID for the authenticated user.
#### Authentication
Required (JWT Bearer token)
#### Request Body
None
#### Success Response
```json
{
  "message": "Collaborator removed successfully"
}
```
#### Error Responses
* `401 Unauthorized`: Invalid token
* `404 Not Found`: Project not found
* `500 Internal Server Error`: Server error
#### Example Request/Response Pair
```bash
curl -X DELETE \
  https://api.codepal.io/v1/projects/project-1/collaborators/john.doe@example.com \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
```
```json
{
  "message": "Collaborator removed successfully"
}
```