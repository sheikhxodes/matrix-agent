# Matrix Agent

General-purpose AI agent built with Google ADK for complex, long-horizon tasks.

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/template/new?template=https://github.com/sheikhxodes/matrix-agent)

## Features

| Capability | Description |
|------------|-------------|
| **Code** | Full-stack web apps with Auth, Database, Stripe, E2E testing |
| **PPT** | Beautiful presentations with flexible layouts and PPTX export |
| **Deep Research** | Web search, APIs, browser automation, data analysis |
| **Multimodal** | Image/audio/video understanding and generation |
| **Browser** | Automation via Chrome DevTools Protocol (CDP) |
| **MCP Integration** | Chrome DevTools, Playwright, Railway |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MATRIX COORDINATOR                       │
│          (Multi-step planning + <think> reasoning)          │
└──────────┬──────────┬──────────┬──────────┬────────────────┘
           │          │          │          │
    ┌──────▼───┐ ┌────▼────┐ ┌───▼────┐ ┌───▼────┐ ┌────────┐
    │  Code    │ │   PPT   │ │Research│ │  Multi │ │Browser │
    │  Agent   │ │  Agent  │ │ Agent  │ │  modal │ │ Agent  │
    └──────────┘ └─────────┘ └────────┘ └────────┘ └────────┘
```

## Interleaved Thinking

Uses `<think>...</think>` tags to preserve reasoning in conversation history:

```
<think>
Breaking down the task:
1. User wants a SaaS dashboard
2. Need auth → use Supabase
3. Need payments → integrate Stripe
</think>

I'll build your SaaS dashboard with the following plan...
```

## Quick Deploy

### Railway (Recommended)
[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/template/new?template=https://github.com/sheikhxodes/matrix-agent)

### Environment Variables
Set `GOOGLE_API_KEY` in your deployment environment.

## Local Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Set API key
export GOOGLE_API_KEY="your-key"

# Run CLI
python main.py

# Run API server
uvicorn main:app --reload
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/chat` | POST | Quick chat |
| `/sessions` | POST/GET | Create/list sessions |
| `/sessions/{id}` | GET/PUT/DELETE | Session CRUD |
| `/sessions/{id}/messages` | POST/GET | Messages CRUD |

## Project Structure

```
matrix-agent/
├── main.py               # FastAPI + CLI entry point
├── Dockerfile            # Container config
├── railway.toml          # Railway deployment config
├── mcp.json              # MCP servers config
├── agents/
│   ├── coordinator.py    # Main coordinator + specialists
│   └── browser_agent.py  # CDP browser automation
└── tools/
    ├── code_tools.py     # Web development tools
    ├── ppt_tools.py      # Presentation tools
    ├── research_tools.py # Research & analysis tools
    ├── multimodal_tools.py # Media processing tools
    └── chrome_devtools_tools.py # Browser automation
```

## MCP Servers

```json
{
  "mcpServers": {
    "chrome-devtools": { "command": "npx", "args": ["chrome-devtools-mcp@latest"] },
    "playwright": { "command": "npx", "args": ["@playwright/mcp@latest"] },
    "railway": { "command": "npx", "args": ["-y", "@railway/mcp-server"] }
  }
}
```

## License

Apache 2.0
