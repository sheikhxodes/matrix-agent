<div align="center">

<img src="assets/logo-banner.svg" alt="MATRIX" width="100%">

<br>
<br>

# Matrix Agent

**Enterprise-Grade AI Agent Platform**

*Multi-agent orchestration with interleaved thinking, tool use, and API compatibility*

<br>

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/template/new?template=https://github.com/sheikhxodes/matrix-agent)
&nbsp;&nbsp;
[![Documentation](https://img.shields.io/badge/docs-MkDocs-blue?style=flat-square)](https://sheikhxodes.github.io/matrix-agent)
&nbsp;&nbsp;
[![License](https://img.shields.io/badge/license-Apache%202.0-green?style=flat-square)](LICENSE)

<br>

[Features](#features) • [Quick Start](#quick-start) • [API Reference](#api-reference) • [Documentation](https://sheikhxodes.github.io/matrix-agent)

</div>

---

## Overview

Matrix Agent is a **general-purpose AI platform** built on Google ADK that orchestrates specialized agents to complete complex, long-horizon tasks. It provides **Anthropic and OpenAI compatible APIs**, making it a drop-in replacement for existing applications.

<br>

## Features

<table>
<tr>
<td width="50%">

### 🤖 Multi-Agent System
- **Coordinator** - Orchestrates all specialists
- **Code Agent** - Full-stack development
- **PPT Agent** - Presentation design
- **Research Agent** - Deep research & analysis
- **Multimodal Agent** - Image/audio/video
- **Browser Agent** - Web automation

</td>
<td width="50%">

### ⚡ Advanced Capabilities
- **Interleaved Thinking** - `<think>` reasoning blocks
- **Tool Use** - Dynamic tool integration
- **Prompt Caching** - Optimized responses
- **Code Understanding** - Explain, review, refactor
- **MCP Integration** - Extensible via MCP servers

</td>
</tr>
</table>

<br>

## API Compatibility

| API | Endpoint | Status |
|-----|----------|--------|
| **Anthropic Messages** | `/anthropic/v1/messages` | ✅ Recommended |
| **OpenAI Chat** | `/v1/chat/completions` | ✅ Supported |
| **Code Assistant** | `/v1/code` | ✅ Supported |
| **Models** | `/v1/models` | ✅ Supported |

<br>

## Quick Start

### One-Click Deploy

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/template/new?template=https://github.com/sheikhxodes/matrix-agent)

### Local Installation

```bash
# Clone repository
git clone https://github.com/sheikhxodes/matrix-agent.git
cd matrix-agent

# Install dependencies
pip install -r requirements.txt

# Configure environment
export GOOGLE_API_KEY="your-api-key"

# Start server
uvicorn main:app --reload
```

<br>

## API Reference

### Anthropic Messages API (Recommended)

```bash
curl -X POST http://localhost:8000/anthropic/v1/messages \
  -H "Content-Type: application/json" \
  -H "anthropic-version: 2024-01-01" \
  -d '{
    "model": "matrix-agent",
    "max_tokens": 4096,
    "messages": [
      {"role": "user", "content": "Build a React dashboard with auth"}
    ]
  }'
```

### OpenAI Chat Completions

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

<br>

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        MATRIX COORDINATOR                           │
│              Multi-step Planning + Interleaved Thinking             │
└─────────────────────────────────────────────────────────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │           │             │             │           │
    ┌────▼────┐ ┌────▼────┐ ┌──────▼──────┐ ┌────▼────┐ ┌────▼────┐
    │  Code   │ │   PPT   │ │  Research   │ │  Multi  │ │ Browser │
    │  Agent  │ │  Agent  │ │    Agent    │ │  modal  │ │  Agent  │
    └─────────┘ └─────────┘ └─────────────┘ └─────────┘ └─────────┘
```

<br>

## Interleaved Thinking

Matrix Agent preserves reasoning in `<think>` blocks:

```xml
<think>
Analyzing the request:
1. User needs a SaaS dashboard
2. Requires authentication → Supabase
3. Needs payments → Stripe integration
4. Frontend → Next.js with Tailwind
</think>

I'll build your SaaS dashboard with the following architecture...
```

<br>

## MCP Servers

Extend functionality with Model Context Protocol servers:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest"]
    },
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    },
    "railway": {
      "command": "npx",
      "args": ["-y", "@railway/mcp-server"]
    }
  }
}
```

<br>

## Project Structure

```
matrix-agent/
├── main.py                 # FastAPI application
├── agents/
│   ├── coordinator.py      # Main orchestrator
│   └── browser_agent.py    # Browser automation
├── tools/
│   ├── code_tools.py       # Development tools
│   ├── ppt_tools.py        # Presentation tools
│   ├── research_tools.py   # Research tools
│   └── multimodal_tools.py # Media tools
├── docs/                   # MkDocs documentation
├── assets/                 # Branding assets
└── mcp.json               # MCP configuration
```

<br>

## Documentation

Full documentation available at **[sheikhxodes.github.io/matrix-agent](https://sheikhxodes.github.io/matrix-agent)**

<br>

---

<div align="center">

<img src="assets/footer-banner.svg" alt="MATRIX" width="400">

<br>
<br>

**Created by [Likhon Sheikh](https://t.me/likhonsheikh)**

[![Telegram](https://img.shields.io/badge/Telegram-@likhonsheikh-blue?style=flat-square&logo=telegram)](https://t.me/likhonsheikh)
[![GitHub](https://img.shields.io/badge/GitHub-@sheikhxodes-black?style=flat-square&logo=github)](https://github.com/sheikhxodes)

<br>

**Apache 2.0 License**

</div>
