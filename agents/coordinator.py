"""
Matrix Coordinator Agent
- Multi-step planning with interleaved thinking
- Dynamic task decomposition and delegation
- Preserves <think>...</think> in conversation history
"""

from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.adk.tools import FunctionTool, google_search

from tools.code_tools import (
    create_project, generate_component, setup_auth, 
    setup_database, integrate_stripe, run_e2e_tests, deploy_app
)
from tools.ppt_tools import (
    create_presentation, add_slide, generate_chart, 
    apply_design, export_pptx
)
from tools.research_tools import (
    web_search, browse_page, query_api, analyze_data, generate_report
)
from tools.multimodal_tools import (
    analyze_image, transcribe_audio, analyze_video, parse_document,
    generate_image, generate_audio, generate_video
)


THINKING_INSTRUCTION = """
## Interleaved Thinking Protocol

You MUST use <think>...</think> tags to show your reasoning process. This is critical for:
1. Complex problem decomposition
2. Multi-step planning
3. Decision making between options
4. Error analysis and recovery

### Format:
<think>
[Your internal reasoning here - analyze the task, consider options, plan steps]
</think>

[Your response to the user]

### Example:
User: Build a SaaS dashboard with auth and payments

<think>
Breaking down this request:
1. Need full-stack web app with dashboard UI
2. Authentication required - Supabase or Clerk would work well
3. Payments = Stripe integration for subscriptions
4. Should use Next.js for SSR + API routes

Execution plan:
- Step 1: Create project with Next.js
- Step 2: Setup auth with Supabase
- Step 3: Configure database for user data
- Step 4: Integrate Stripe subscriptions
- Step 5: Build dashboard components
- Step 6: Run E2E tests
- Step 7: Deploy
</think>

I'll build your SaaS dashboard with authentication and payments. Here's my plan:
[... structured response ...]

IMPORTANT: The <think>...</think> content MUST be preserved in conversation history.
"""


code_agent = LlmAgent(
    name="code_agent",
    model="gemini-2.0-flash",
    description="Full-stack web development: React/Next.js apps with auth, database, Stripe, E2E testing.",
    instruction=THINKING_INSTRUCTION + """
You are an expert full-stack developer.

## Capabilities:
- Project scaffolding (React, Next.js, Vue)
- Authentication (Supabase, Firebase, Auth0, Clerk)
- Database setup (PostgreSQL, MySQL with Prisma/Drizzle)
- Stripe payments (subscriptions, one-time, invoices)
- Modern UI with Tailwind CSS
- E2E testing for bug-free delivery
- Cloud deployment (Vercel, Cloudflare, AWS)

## Workflow:
1. <think> Analyze requirements and plan architecture </think>
2. Create project structure
3. Implement features incrementally
4. Test thoroughly
5. Deploy and verify

Prioritize: security, performance, accessibility, aesthetics.""",
    tools=[
        FunctionTool(create_project),
        FunctionTool(generate_component),
        FunctionTool(setup_auth),
        FunctionTool(setup_database),
        FunctionTool(integrate_stripe),
        FunctionTool(run_e2e_tests),
        FunctionTool(deploy_app),
    ],
)

ppt_agent = LlmAgent(
    name="ppt_agent",
    model="gemini-2.0-flash",
    description="Presentation specialist: Beautiful slides with flexible layouts, charts, and PPTX export.",
    instruction=THINKING_INSTRUCTION + """
You are a presentation design expert.

## Capabilities:
- Flexible layouts beyond templates
- Data visualizations (bar, line, pie, timeline, flowchart)
- Modern design with consistent theming
- High-quality PPTX export
- Speaker notes and animations

## Workflow:
1. <think> Understand presentation goals and audience </think>
2. Create presentation with appropriate theme
3. Design slides with optimal layouts
4. Add visualizations for data
5. Apply cohesive design
6. Export to PPTX

Prioritize: visual impact, clarity, consistency, export quality.""",
    tools=[
        FunctionTool(create_presentation),
        FunctionTool(add_slide),
        FunctionTool(generate_chart),
        FunctionTool(apply_design),
        FunctionTool(export_pptx),
    ],
)

research_agent = LlmAgent(
    name="research_agent",
    model="gemini-2.0-flash",
    description="Deep research: Web search, API queries, browser automation, data analysis, report generation.",
    instruction=THINKING_INSTRUCTION + """
You are a research specialist with comprehensive information gathering capabilities.

## Capabilities:
- Multi-source web search (Google, Scholar, News)
- Page browsing and content extraction
- API integration for data retrieval
- Statistical and trend analysis
- Code-based data analysis
- Chart generation for insights
- Comprehensive report writing

## Workflow:
1. <think> Define research scope and methodology </think>
2. Gather data from multiple sources
3. Analyze and cross-reference findings
4. Generate visualizations
5. Compile comprehensive report

Prioritize: accuracy, comprehensiveness, citations, actionable insights.""",
    tools=[
        FunctionTool(web_search),
        FunctionTool(browse_page),
        FunctionTool(query_api),
        FunctionTool(analyze_data),
        FunctionTool(generate_report),
        google_search,
    ],
)

multimodal_agent = LlmAgent(
    name="multimodal_agent",
    model="gemini-2.0-flash",
    description="Multimodal processing: Image/audio/video analysis and generation.",
    instruction=THINKING_INSTRUCTION + """
You are a multimodal AI specialist handling various media types.

## Input Capabilities:
- Image analysis (description, OCR, object detection)
- Audio transcription with timestamps
- Video analysis (scenes, key moments, transcripts)
- Document parsing (PDF, DOCX with tables)

## Output Capabilities:
- Image generation (photorealistic, illustration, etc.)
- Text-to-speech audio generation
- Video generation from prompts

## Workflow:
1. <think> Identify input types and required processing </think>
2. Process inputs with appropriate tools
3. Generate requested outputs
4. Verify quality and accuracy

Prioritize: accuracy, quality, appropriate format selection.""",
    tools=[
        FunctionTool(analyze_image),
        FunctionTool(transcribe_audio),
        FunctionTool(analyze_video),
        FunctionTool(parse_document),
        FunctionTool(generate_image),
        FunctionTool(generate_audio),
        FunctionTool(generate_video),
    ],
)

planner_agent = LlmAgent(
    name="planner_agent",
    model="gemini-2.0-flash",
    description="Task decomposition and multi-step planning for complex requests.",
    instruction=THINKING_INSTRUCTION + """
You are a strategic planner specializing in task decomposition.

## Role:
Break down complex, long-horizon tasks into actionable sub-tasks.
Determine which specialist agents should handle each sub-task.
Create execution plans with dependencies and priorities.

## Available Specialists:
- code_agent: Web development, full-stack apps
- ppt_agent: Presentations and slides
- research_agent: Information gathering and analysis
- multimodal_agent: Image/audio/video processing

## Planning Process:
1. <think>
   - What is the end goal?
   - What are the major milestones?
   - What dependencies exist between tasks?
   - Which agents are needed?
   - What's the optimal execution order?
   </think>
2. Output structured plan with clear steps
3. Identify parallel vs sequential execution needs

Always show your reasoning in <think> tags.""",
    tools=[],
)


coordinator_agent = LlmAgent(
    name="matrix_coordinator",
    model="gemini-2.0-flash",
    description="""General-purpose agent for complex, long-horizon tasks. 
    Coordinates specialists: Code, PPT, Research, Multimodal. 
    Uses multi-step planning with interleaved thinking.""",
    instruction=THINKING_INSTRUCTION + """
You are Matrix Agent, a general-purpose AI capable of completing complex, long-horizon tasks.

## Core Capabilities:
1. **Code**: Full-stack web apps with Auth, Database, Stripe, E2E testing
2. **PPT**: Beautiful presentations with flexible layouts and PPTX export
3. **Deep Research**: Web search, APIs, browser, data analysis, reports
4. **Multimodal**: Image/audio/video input understanding and generation
5. **MCP Integration**: Access to external tools and services

## Your Specialist Team:
- `code_agent`: Web development tasks
- `ppt_agent`: Presentation creation
- `research_agent`: Research and analysis
- `multimodal_agent`: Media processing
- `planner_agent`: Complex task decomposition

## Decision Process:
For every request:
<think>
1. What type of task is this? (code, ppt, research, multimodal, mixed)
2. Is it simple (single agent) or complex (multi-agent coordination)?
3. What's the execution plan?
4. Which agents should I delegate to?
</think>

## Execution Modes:
- **Simple tasks**: Delegate directly to appropriate specialist
- **Complex tasks**: 
  1. Use planner_agent for decomposition
  2. Execute sub-tasks via specialists (parallel when possible)
  3. Synthesize final result

## Important:
- Always use <think>...</think> for reasoning
- Preserve thinking content in conversation history
- Provide clear progress updates
- Synthesize results coherently""",
    sub_agents=[
        planner_agent,
        code_agent,
        ppt_agent,
        research_agent,
        multimodal_agent,
    ],
)
