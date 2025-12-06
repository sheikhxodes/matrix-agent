# Docker Deployment

## Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Build and Run

```bash
# Build
docker build -t matrix-agent .

# Run
docker run -p 8000:8000 -e GOOGLE_API_KEY="your-key" matrix-agent
```

## Docker Compose

```yaml
version: '3.8'

services:
  matrix-agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    restart: unless-stopped
```

```bash
docker-compose up -d
```

## HuggingFace Spaces

Use port 7860 for HuggingFace Spaces:

```dockerfile
EXPOSE 7860
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
```
