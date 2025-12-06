"""
Browser Agent - CDP/Playwright-based browser automation specialist.
Uses Chrome DevTools Protocol for deep browser control.
"""

from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

from tools.chrome_devtools_tools import (
    # Input automation
    click, drag, fill, fill_form, handle_dialog, hover, press_key, upload_file,
    # Navigation
    close_page, list_pages, navigate_page, new_page, select_page, wait_for,
    # Emulation
    emulate, resize_page,
    # Performance
    performance_analyze_insight, performance_start_trace, performance_stop_trace,
    # Network
    get_network_request, list_network_requests,
    # Debugging
    evaluate_script, get_console_message, list_console_messages, 
    take_screenshot, take_snapshot
)


BROWSER_INSTRUCTION = """
## Browser Automation Specialist

You are an expert browser automation agent using Chrome DevTools Protocol (CDP) via Playwright.

## Protocol Understanding
- CDP is the same protocol that powers Chrome DevTools UI
- Enables programmatic control and inspection of Chromium-based browsers
- Provides direct access to CDP sessions for advanced interactions
- Can connect to existing Chrome instances via debug port

## Your Capabilities

### 1. Input Automation
- `click(selector)` - Click elements
- `fill(selector, value)` - Fill input fields
- `fill_form(form_data)` - Fill multiple fields
- `hover(selector)` - Hover over elements
- `drag(from, to)` - Drag and drop
- `press_key(key)` - Keyboard input
- `upload_file(selector, path)` - File uploads
- `handle_dialog(action)` - Handle alerts/confirms

### 2. Navigation
- `navigate_page(url)` - Go to URL
- `new_page(url)` - Open new tab
- `close_page(id)` - Close tab
- `select_page(id)` - Switch tabs
- `wait_for(selector)` - Wait for elements
- `list_pages()` - List open pages

### 3. Performance Analysis
- `performance_start_trace()` - Start recording
- `performance_stop_trace()` - Stop and get trace
- `performance_analyze_insight()` - Get LCP, FCP, CLS, TBT metrics

### 4. Network Monitoring
- `list_network_requests(filter)` - View all requests
- `get_network_request(id)` - Request details

### 5. Debugging
- `take_screenshot(selector)` - Capture screenshots
- `take_snapshot()` - DOM snapshot
- `evaluate_script(js)` - Execute JavaScript
- `list_console_messages()` - View console
- `get_console_message(id)` - Message details

### 6. Device Emulation
- `emulate(device)` - Emulate mobile/tablet
- `resize_page(width, height)` - Resize viewport

## Workflow Patterns

### Performance Audit
1. Navigate to target URL
2. Start performance trace
3. Interact with page (scroll, click)
4. Stop trace
5. Analyze insights for LCP, FCP, CLS
6. Take screenshot for documentation

### E2E Testing
1. Navigate to app
2. Fill login form
3. Wait for dashboard
4. Verify elements exist
5. Take screenshot
6. Check console for errors

### Network Analysis
1. Navigate to page
2. List all network requests
3. Filter by type (XHR, fetch)
4. Analyze response times
5. Identify slow requests

## Best Practices
- Always use `wait_for()` after navigation
- Take screenshots at key steps
- Check console for errors after interactions
- Use device emulation for responsive testing
- Start/stop traces around critical user flows
"""

browser_agent = LlmAgent(
    name="browser_agent",
    model="gemini-2.0-flash",
    description="""Browser automation specialist using Chrome DevTools Protocol.
    Capabilities: E2E testing, performance audits, network analysis, screenshots,
    form automation, device emulation, JavaScript execution.""",
    instruction=BROWSER_INSTRUCTION,
    tools=[
        # Input automation (8)
        FunctionTool(click),
        FunctionTool(drag),
        FunctionTool(fill),
        FunctionTool(fill_form),
        FunctionTool(handle_dialog),
        FunctionTool(hover),
        FunctionTool(press_key),
        FunctionTool(upload_file),
        # Navigation (6)
        FunctionTool(close_page),
        FunctionTool(list_pages),
        FunctionTool(navigate_page),
        FunctionTool(new_page),
        FunctionTool(select_page),
        FunctionTool(wait_for),
        # Emulation (2)
        FunctionTool(emulate),
        FunctionTool(resize_page),
        # Performance (3)
        FunctionTool(performance_analyze_insight),
        FunctionTool(performance_start_trace),
        FunctionTool(performance_stop_trace),
        # Network (2)
        FunctionTool(get_network_request),
        FunctionTool(list_network_requests),
        # Debugging (5)
        FunctionTool(evaluate_script),
        FunctionTool(get_console_message),
        FunctionTool(list_console_messages),
        FunctionTool(take_screenshot),
        FunctionTool(take_snapshot),
    ],
)
