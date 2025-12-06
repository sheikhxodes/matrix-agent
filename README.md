<p align="center">
  <img src="assets/logo.svg" alt="Matrix Agent" width="300">
</p>

<h1 align="center">Matrix Agent</h1>

<p align="center">
  <strong>General-purpose AI Agent for complex, long-horizon tasks</strong><br>
  Built with Google ADK • Powered by Gemini • By <a href="https://t.me/likhonsheikh">Likhon Sheikh</a>
</p>

<p align="center">
  <a href="https://railway.com/template/new?template=https://github.com/sheikhxodes/matrix-agent">
    <img src="https://railway.com/button.svg" alt="Deploy on Railway">
  </a>
</p>

---

## Features

| Capability | Description |
|------------|-------------|
| **Code** | Full-stack web apps with Auth, Database, Stripe, E2E testing |
| **PPT** | Beautiful presentations with flexible layouts and PPTX export |
| **Deep Research** | Web search, APIs, browser automation, data analysis |
| **Multimodal** | Image/audio/video understanding and generation |
| **Browser** | Automation via Chrome DevTools Protocol (CDP) |
| **MCP Integration** | Chrome DevTools, Playwright, Railway |

## API Compatibility

| API | Endpoint | Description |
|-----|----------|-------------|
| **Anthropic** (Recommended) | `/anthropic/v1/messages` | Full Messages API with thinking blocks |
| **OpenAI** | `/v1/chat/completions` | Chat Completions compatible |
| **Code Assistant** | `/v1/code` | Specialized code understanding |

### Advanced Features
- **Interleaved Thinking** - `<think>...</think>` blocks preserved
- **Tool Use** - Pass tools in requests
- **Prompt Caching** - Automatic caching for repeated requests
- **Code Understanding** - explain, review, refactor, debug, complete

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

## Quick Start

### Deploy on Railway
[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/template/new?template=https://github.com/sheikhxodes/matrix-agent)

### Local Installation

```bash
# Clone
git clone https://github.com/sheikhxodes/matrix-agent.git
cd matrix-agent

# Install
pip install -r requirements.txt

# Set API key
export GOOGLE_API_KEY="your-key"

# Run
uvicorn main:app --reload
```

## Usage Examples

### Anthropic API (Recommended)
```bash
curl -X POST http://localhost:8000/anthropic/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "matrix-agent",
    "messages": [{"role": "user", "content": "Build a React dashboard"}],
    "max_tokens": 4096
  }'
```

### OpenAI API
```bash
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "matrix-agent",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### Code Assistant
```bash
curl -X POST http://localhost:8000/v1/code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def factorial(n): return 1 if n <= 1 else n * factorial(n-1)",
    "task": "explain",
    "language": "python"
  }'
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/anthropic/v1/messages` | POST | Anthropic Messages API |
| `/v1/chat/completions` | POST | OpenAI Chat API |
| `/v1/code` | POST | Code assistant |
| `/v1/models` | GET | List models |
| `/chat` | POST | Quick chat |
| `/sessions` | POST/GET | Session management |
| `/health` | GET | Health check |

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

## Documentation

📚 [Full Documentation](https://sheikhxodes.github.io/matrix-agent)

## Author

**Likhon Sheikh**
- Telegram: [@likhonsheikh](https://t.me/likhonsheikh)
- GitHub: [@sheikhxodes](https://github.com/sheikhxodes)

## License

Apache 2.0
