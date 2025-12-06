# API Endpoints

## Base URL

```
http://localhost:8000
```

## Health Check

```http
GET /health
```

**Response:**
```json
{"status": "healthy", "agent": "matrix_coordinator"}
```

## Quick Chat

```http
POST /chat
Content-Type: application/json

{"message": "Your message here"}
```

**Response:**
```json
{
  "response": "Agent response with <think>...</think> tags",
  "session_id": null
}
```

## Sessions

### Create Session

```http
POST /sessions
Content-Type: application/json

{"name": "my-session"}
```

### List Sessions

```http
GET /sessions
GET /sessions?skip=0&limit=10
```

### Get Session

```http
GET /sessions/{session_id}
```

### Update Session

```http
PUT /sessions/{session_id}
Content-Type: application/json

{"name": "updated-name"}
```

### Delete Session

```http
DELETE /sessions/{session_id}
```

## Messages

### Send Message

```http
POST /sessions/{session_id}/messages
Content-Type: application/json

{"message": "Your message"}
```

### Get Messages

```http
GET /sessions/{session_id}/messages
```

### Delete Message

```http
DELETE /sessions/{session_id}/messages/{message_id}
```
