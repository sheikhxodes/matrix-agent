# Agents

## Coordinator Agent

The main orchestrator that coordinates all specialist agents.

```python
coordinator_agent = LlmAgent(
    name="matrix_coordinator",
    model="gemini-2.0-flash",
    description="General-purpose agent for complex tasks",
    instruction=THINKING_INSTRUCTION + "...",
    sub_agents=[planner, code, ppt, research, multimodal, browser],
)
```

## Planner Agent

Breaks down complex tasks into actionable sub-tasks.

**Capabilities:**

- Task decomposition
- Dependency analysis
- Parallel vs sequential planning
- Agent assignment

## Code Agent

Full-stack web development specialist.

**Capabilities:**

- React/Next.js/Vue projects
- Authentication (Supabase, Firebase, Clerk)
- Database setup (PostgreSQL, MySQL)
- Stripe payments
- E2E testing
- Cloud deployment

## PPT Agent

Presentation design expert.

**Capabilities:**

- Flexible slide layouts
- Data visualizations
- Modern theming
- PPTX export

## Research Agent

Information gathering and analysis.

**Capabilities:**

- Web search
- Page browsing
- API queries
- Data analysis
- Report generation

## Multimodal Agent

Media processing specialist.

**Input:** Image, audio, video, document analysis  
**Output:** Image, audio, video generation

## Browser Agent

Web automation via Chrome DevTools Protocol.

**Capabilities:**

- Navigation and interaction
- Screenshots and snapshots
- Performance tracing
- Network monitoring
- Console debugging
