# MCP Servers

## Configured Servers

### Chrome DevTools

```json
{
  "chrome-devtools": {
    "command": "npx",
    "args": ["chrome-devtools-mcp@latest"]
  }
}
```

**Capabilities:**

- Browser automation via CDP
- Screenshots and snapshots
- Performance profiling
- Network monitoring
- Console debugging

### Playwright

```json
{
  "playwright": {
    "command": "npx",
    "args": ["@playwright/mcp@latest"]
  }
}
```

**Capabilities:**

- Cross-browser testing
- Page interactions
- Screenshot capture
- PDF generation

### Railway

```json
{
  "railway": {
    "command": "npx",
    "args": ["-y", "@railway/mcp-server"]
  }
}
```

**Capabilities:**

- Deploy services
- Manage projects
- Environment variables
- Logs and metrics

## Adding New Servers

1. Find MCP-compatible server package
2. Add to `mcp.json`:

```json
{
  "new-server": {
    "command": "npx",
    "args": ["package-name"]
  }
}
```

3. Restart the agent

## Popular MCP Servers

- `@anthropic/mcp-server-filesystem`
- `@anthropic/mcp-server-github`
- `@anthropic/mcp-server-memory`
