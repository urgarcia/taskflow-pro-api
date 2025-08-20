# 📋 API Documentation

## Base URL
```
Production: https://e7j8m0r1hf.execute-api.us-east-1.amazonaws.com/dev
Local:      http://localhost:5000
```

## Authentication
All protected endpoints require JWT token from AWS Cognito in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

---

## 🏠 Health Check

### GET /
Check if the API is running

**Response:**
```json
{
  "status": "ok",
  "message": "API funcionando correctamente"
}
```

**Status Codes:**
- `200` - Success

---

## 👤 Authentication Endpoints

### POST /register
Register a new user

**Request Body:**
```json
{
  "username": "string",
  "password": "string",
  "name": "string" (optional)
}
```

**Response:**
```json
{
  "id": 1,
  "username": "johndoe",
  "name": "John Doe"
}
```

**Status Codes:**
- `201` - User created successfully
- `400` - Bad request (missing username or password)
- `409` - Conflict (username already exists)

---

### POST /login
Login user (Reference - Use AWS Cognito instead)

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "msg": "Use AWS Cognito para autenticarse. Esta ruta es solo para referencia.",
  "info": "El frontend debe autenticarse con Cognito y enviar el token en Authorization header"
}
```

**Status Codes:**
- `200` - Information message

---

### GET /profile 🔒
Get current user profile

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "msg": "Profile data from Cognito JWT",
  "user": {
    "id": "cognito-user-id",
    "username": "cognito:username",
    "email": "user@example.com",
    "token_use": "access",
    "client_id": "cognito-client-id"
  }
}
```

**Status Codes:**
- `200` - Success
- `401` - Unauthorized (invalid or missing token)

---

## 📋 Task Endpoints

### GET /tasks 🔒
Get all tasks

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Response:**
```json
[
  {
    "id": 1,
    "title": "Complete project",
    "description": "Finish the task management API",
    "completed": false
  },
  {
    "id": 2,
    "title": "Write documentation",
    "description": "Create API documentation",
    "completed": true
  }
]
```

**Status Codes:**
- `200` - Success
- `401` - Unauthorized

---

### GET /tasks/{id} 🔒
Get a specific task by ID

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Path Parameters:**
- `id` (integer) - Task ID

**Response:**
```json
{
  "id": 1,
  "title": "Complete project",
  "description": "Finish the task management API",
  "completed": false
}
```

**Status Codes:**
- `200` - Success
- `401` - Unauthorized
- `404` - Task not found

---

### POST /tasks 🔒
Create a new task

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "string" (required),
  "description": "string" (optional)
}
```

**Response:**
```json
{
  "id": 3,
  "title": "New task",
  "description": "Task description",
  "completed": false
}
```

**Status Codes:**
- `201` - Task created successfully
- `400` - Bad request (missing title)
- `401` - Unauthorized

---

### PUT /tasks/{id} 🔒
Update an existing task

**Headers:**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**Path Parameters:**
- `id` (integer) - Task ID

**Request Body:**
```json
{
  "title": "string" (optional),
  "description": "string" (optional),
  "completed": boolean (optional)
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Updated task",
  "description": "Updated description",
  "completed": true
}
```

**Status Codes:**
- `200` - Task updated successfully
- `401` - Unauthorized
- `404` - Task not found

---

### DELETE /tasks/{id} 🔒
Delete a task

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Path Parameters:**
- `id` (integer) - Task ID

**Response:**
```
(Empty response body)
```

**Status Codes:**
- `204` - Task deleted successfully
- `401` - Unauthorized
- `404` - Task not found

---

## 🔧 Error Responses

All endpoints may return the following error formats:

### 400 Bad Request
```json
{
  "error": "Title is required"
}
```

### 401 Unauthorized
```json
{
  "error": "Token de autorización requerido"
}
```

```json
{
  "error": "Token inválido o expirado"
}
```

### 404 Not Found
```json
{
  "error": "Task not found"
}
```

---

## 📝 Data Models

### Task Model
```json
{
  "id": "integer",
  "title": "string (max 128 chars)",
  "description": "string (text)",
  "completed": "boolean (default: false)"
}
```

### User Model
```json
{
  "id": "integer",
  "username": "string (max 64 chars, unique)",
  "name": "string (max 128 chars, optional)"
}
```

### Cognito JWT Payload
```json
{
  "id": "string (sub)",
  "username": "string (cognito:username)",
  "email": "string",
  "token_use": "string (access|id)",
  "client_id": "string",
  "iss": "string (issuer)",
  "aud": "string (audience)",
  "exp": "number (expiration)",
  "iat": "number (issued at)"
}
```

---

## 🚀 Examples

### JavaScript/TypeScript Examples

#### Authentication with AWS Cognito
```typescript
import { Auth } from 'aws-amplify';

// Configure Amplify (do this once in your app)
Auth.configure({
  region: 'us-east-1',
  userPoolId: 'us-east-1_Zo904D2He',
  userPoolWebClientId: '1u6mep85s45jigl31n5ijnqkui'
});

// Sign in
const session = await Auth.signIn(username, password);
const token = session.getAccessToken().getJwtToken();
```

#### API Calls
```typescript
const API_BASE = 'https://e7j8m0r1hf.execute-api.us-east-1.amazonaws.com/dev';

// Get all tasks
const getTasks = async (token: string) => {
  const response = await fetch(`${API_BASE}/tasks`, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  return response.json();
};

// Create a task
const createTask = async (token: string, task: {title: string, description?: string}) => {
  const response = await fetch(`${API_BASE}/tasks`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(task)
  });
  return response.json();
};

// Update a task
const updateTask = async (token: string, id: number, updates: any) => {
  const response = await fetch(`${API_BASE}/tasks/${id}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(updates)
  });
  return response.json();
};

// Delete a task
const deleteTask = async (token: string, id: number) => {
  await fetch(`${API_BASE}/tasks/${id}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
};
```

### cURL Examples

#### Get all tasks
```bash
curl -X GET \
  "https://e7j8m0r1hf.execute-api.us-east-1.amazonaws.com/dev/tasks" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

#### Create a task
```bash
curl -X POST \
  "https://e7j8m0r1hf.execute-api.us-east-1.amazonaws.com/dev/tasks" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Task",
    "description": "Task description"
  }'
```

#### Update a task
```bash
curl -X PUT \
  "https://e7j8m0r1hf.execute-api.us-east-1.amazonaws.com/dev/tasks/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Task",
    "completed": true
  }'
```

#### Delete a task
```bash
curl -X DELETE \
  "https://e7j8m0r1hf.execute-api.us-east-1.amazonaws.com/dev/tasks/1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## 🔒 Security Considerations

1. **JWT Tokens**: All tokens are validated against AWS Cognito's public keys
2. **HTTPS Only**: All production endpoints use HTTPS
3. **CORS**: Configured to allow cross-origin requests for development
4. **Input Validation**: All inputs are validated before processing
5. **Error Handling**: Sensitive information is not exposed in error messages

---

## 📊 Rate Limiting

Currently, no rate limiting is implemented. Consider implementing rate limiting for production use.

---

## 🐛 Troubleshooting

### Common Issues

1. **401 Unauthorized**: Check that your JWT token is valid and not expired
2. **404 Not Found**: Verify the endpoint URL and task ID
3. **CORS Errors**: Ensure your frontend domain is allowed in CORS settings
4. **500 Internal Server Error**: Check server logs with `zappa tail dev`

### Getting Help

For issues or questions:
1. Check the server logs: `zappa tail dev`
2. Verify your JWT token is valid
3. Ensure all required fields are provided in requests
4. Check that the database connection is working

---

*Last updated: August 2025*
