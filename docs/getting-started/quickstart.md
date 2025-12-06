# Quick Start

## Running the API Server

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## Quick Chat

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello Matrix Agent!"}'
```

## Create a Session

```bash
# Create session
curl -X POST http://localhost:8000/sessions \
  -H "Content-Type: application/json" \
  -d '{"name": "my-session"}'

# Response: {"id": "uuid", "name": "my-session", ...}
```

## Send Messages

```bash
# Send message to session
curl -X POST http://localhost:8000/sessions/{session_id}/messages \
  -H "Content-Type: application/json" \
  -d '{"message": "Build me a SaaS dashboard with auth"}'
```

## CLI Mode

```bash
python main.py

# Interactive prompt:
# You: Build a landing page
# Agent: <think>...</think> I'll create...
```

## Example Tasks

| Task | Agent Used |
|------|------------|
| "Build a Next.js app with Stripe" | Code Agent |
| "Create a pitch deck for my startup" | PPT Agent |
| "Research AI trends in 2024" | Research Agent |
| "Analyze this image" | Multimodal Agent |
| "Take a screenshot of google.com" | Browser Agent |
