# Configuration

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GOOGLE_API_KEY` | Yes | Google AI API key for Gemini |
| `PORT` | No | Server port (default: 8000) |

## Model Configuration

By default, Matrix Agent uses `gemini-2.0-flash`. To change:

```python
# In agents/coordinator.py
coordinator_agent = LlmAgent(
    name="matrix_coordinator",
    model="gemini-2.0-pro",  # Change model here
    ...
)
```

## MCP Servers

Configure MCP servers in `mcp.json`:

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

## Adding New Agents

To add a custom agent:

```python
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

custom_agent = LlmAgent(
    name="custom_agent",
    model="gemini-2.0-flash",
    description="Your agent description",
    instruction="Your agent instructions",
    tools=[FunctionTool(your_function)],
)

# Add to coordinator
coordinator_agent = LlmAgent(
    ...
    sub_agents=[..., custom_agent],
)
```
