# Deploy on Railway

## One-Click Deploy

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/template/new?template=https://github.com/sheikhxodes/matrix-agent)

## Manual Deployment

1. Fork the repository
2. Connect to Railway
3. Set environment variable: `GOOGLE_API_KEY`
4. Deploy

## Configuration Files

### railway.toml

```toml
[build]
builder = "dockerfile"
dockerfilePath = "Dockerfile"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
restartPolicyType = "on_failure"
```

### railway.json

```json
{
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/health"
  }
}
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | Yes | Google AI API key |
| `PORT` | Auto | Set by Railway |

## Monitoring

After deployment:

- Check `/health` endpoint
- View logs in Railway dashboard
- Monitor metrics
