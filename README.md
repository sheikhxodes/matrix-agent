# Matrix Agent

General-purpose AI agent built with Google ADK for complex, long-horizon tasks.

## Features

| Capability | Description |
|------------|-------------|
| **Code** | Full-stack web apps with Auth, Database, Stripe, E2E testing |
| **PPT** | Beautiful presentations with flexible layouts and PPTX export |
| **Deep Research** | Web search, APIs, browser automation, data analysis |
| **Multimodal** | Image/audio/video understanding and generation |
| **MCP Integration** | Custom and pre-built MCP tools |

## Architecture

```
┌─────────────────────────────────────────────────────┐
│           MATRIX COORDINATOR                        │
│     (Multi-step planning + <think> reasoning)       │
└──────────┬──────────┬──────────┬───────────────────┘
           │          │          │
    ┌──────▼───┐ ┌────▼────┐ ┌───▼────┐ ┌────────┐
    │  Code    │ │   PPT   │ │Research│ │  Multi │
    │  Agent   │ │  Agent  │ │ Agent  │ │  modal │
    └──────────┘ └─────────┘ └────────┘ └────────┘
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

## Installation

```bash
pip install google-adk google-genai
```

## Usage

```bash
# Set API key
export GOOGLE_API_KEY="your-key"

# Run CLI
cd matrix_agent
python main.py
```

## Project Structure

```
matrix_agent/
├── agents/
│   ├── __init__.py
│   └── coordinator.py    # Main coordinator + specialists
├── tools/
│   ├── __init__.py
│   ├── code_tools.py     # Web development tools
│   ├── ppt_tools.py      # Presentation tools
│   ├── research_tools.py # Research & analysis tools
│   └── multimodal_tools.py # Media processing tools
├── main.py               # CLI entry point
└── pyproject.toml
```

## License

Apache 2.0
