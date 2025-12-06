"""
Matrix Agent - General Purpose AI with Interleaved Thinking
FastAPI Application with Full CRUD + Anthropic/OpenAI Compatible APIs
"""

import asyncio
import os
import re
import uuid
import time
import hashlib
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, Query, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from agents.coordinator import coordinator_agent


# ============== DATA MODELS ==============

@dataclass
class Message:
    id: str
    role: str
    content: str
    thinking: str = ""
    timestamp: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "thinking": self.thinking,
            "timestamp": self.timestamp
        }


@dataclass 
class Session:
    id: str
    name: str
    messages: list = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""
    
    def __post_init__(self):
        now = datetime.utcnow().isoformat()
        if not self.created_at:
            self.created_at = now
        if not self.updated_at:
            self.updated_at = now


# ============== PROMPT CACHE ==============

class PromptCache:
    """Simple prompt cache for repeated requests."""
    def __init__(self, max_size: int = 1000):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def _hash(self, messages: List[Dict], system: str = "") -> str:
        content = str(messages) + system
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def get(self, messages: List[Dict], system: str = "") -> Optional[Dict]:
        key = self._hash(messages, system)
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None
    
    def set(self, messages: List[Dict], system: str, response: Dict):
        if len(self.cache) >= self.max_size:
            oldest = next(iter(self.cache))
            del self.cache[oldest]
        key = self._hash(messages, system)
        self.cache[key] = response
    
    def stats(self) -> Dict:
        return {"hits": self.hits, "misses": self.misses, "size": len(self.cache)}


prompt_cache = PromptCache()


# ============== AGENT CLASS ==============

class MatrixAgent:
    def __init__(self, session_id: str, name: str = ""):
        self.agent = coordinator_agent
        self.session_service = InMemorySessionService()
        self.session = Session(id=session_id, name=name or f"Session-{session_id[:8]}")
        self.adk_session = None
        self.runner = None
    
    async def init(self):
        self.adk_session = await self.session_service.create_session(
            app_name="matrix_agent", user_id=self.session.id
        )
        self.runner = Runner(agent=self.agent, session_service=self.session_service)
        return self
    
    async def chat(self, content: str, system_prompt: str = None) -> Message:
        if not self.runner:
            await self.init()
        
        # User message
        user_msg = Message(id=str(uuid.uuid4()), role="user", content=content)
        self.session.messages.append(user_msg)
        
        # Get response
        response = ""
        async for event in self.runner.run_async(
            session_id=self.adk_session.id,
            user_id=self.session.id,
            new_message=content
        ):
            if hasattr(event, 'content') and event.content:
                response += event.content
        
        # Assistant message
        thinking = ""
        match = re.search(r'<think>(.*?)</think>', response, re.DOTALL)
        if match:
            thinking = match.group(1).strip()
        
        assistant_msg = Message(
            id=str(uuid.uuid4()),
            role="assistant", 
            content=response,
            thinking=thinking
        )
        self.session.messages.append(assistant_msg)
        self.session.updated_at = datetime.utcnow().isoformat()
        
        return assistant_msg


# ============== FASTAPI APP ==============

app = FastAPI(
    title="Matrix Agent API",
    description="General-purpose AI agent with Anthropic & OpenAI compatible APIs",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agents: dict[str, MatrixAgent] = {}


# ============== REQUEST/RESPONSE MODELS ==============

class SessionCreate(BaseModel):
    name: Optional[str] = None

class SessionUpdate(BaseModel):
    name: str

class MessageCreate(BaseModel):
    content: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


# ============== ANTHROPIC API MODELS ==============

class AnthropicMessage(BaseModel):
    role: str
    content: Any  # str or list of content blocks

class AnthropicTool(BaseModel):
    name: str
    description: Optional[str] = None
    input_schema: Optional[Dict] = None

class AnthropicRequest(BaseModel):
    model: str = "matrix-agent"
    messages: List[AnthropicMessage]
    max_tokens: int = 4096
    system: Optional[str] = None
    temperature: Optional[float] = 0.7
    tools: Optional[List[AnthropicTool]] = None
    stream: Optional[bool] = False
    metadata: Optional[Dict] = None


# ============== OPENAI API MODELS ==============

class OpenAIMessage(BaseModel):
    role: str
    content: Optional[str] = None
    name: Optional[str] = None
    tool_calls: Optional[List[Dict]] = None
    tool_call_id: Optional[str] = None

class OpenAITool(BaseModel):
    type: str = "function"
    function: Dict

class OpenAIRequest(BaseModel):
    model: str = "matrix-agent"
    messages: List[OpenAIMessage]
    max_tokens: Optional[int] = 4096
    temperature: Optional[float] = 0.7
    tools: Optional[List[OpenAITool]] = None
    stream: Optional[bool] = False
    n: Optional[int] = 1


# ============== HEALTH & INFO ==============

@app.get("/")
async def root():
    return {
        "name": "Matrix Agent",
        "version": "0.1.0",
        "author": "Likhon Sheikh",
        "capabilities": ["Code", "PPT", "Research", "Multimodal", "Browser"],
        "apis": {
            "native": "/chat, /sessions",
            "anthropic": "/anthropic/v1/messages",
            "openai": "/v1/chat/completions"
        },
        "features": ["interleaved_thinking", "tool_use", "prompt_caching", "code_understanding"],
        "status": "ready"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/v1/models")
@app.get("/anthropic/v1/models")
async def list_models():
    """List available models (OpenAI/Anthropic compatible)."""
    return {
        "object": "list",
        "data": [
            {
                "id": "matrix-agent",
                "object": "model",
                "created": 1700000000,
                "owned_by": "likhon-sheikh",
                "capabilities": ["code", "ppt", "research", "multimodal", "browser"],
                "context_window": 128000
            }
        ]
    }


# ============== ANTHROPIC COMPATIBLE API ==============

@app.post("/anthropic/v1/messages")
async def anthropic_messages(
    request: AnthropicRequest,
    x_api_key: Optional[str] = Header(None, alias="x-api-key"),
    anthropic_version: Optional[str] = Header(None, alias="anthropic-version"),
    anthropic_beta: Optional[str] = Header(None, alias="anthropic-beta")
):
    """
    Anthropic Messages API compatible endpoint.
    Supports: interleaved thinking, tool use, prompt caching.
    """
    start_time = time.time()
    
    # Check cache
    cache_key_messages = [{"role": m.role, "content": str(m.content)} for m in request.messages]
    cached = prompt_cache.get(cache_key_messages, request.system or "")
    if cached and not request.stream:
        cached["cache_hit"] = True
        return cached
    
    # Build conversation
    system_prompt = request.system or ""
    if request.tools:
        tool_desc = "\n".join([f"- {t.name}: {t.description}" for t in request.tools])
        system_prompt += f"\n\nAvailable tools:\n{tool_desc}"
    
    # Get last user message
    user_content = ""
    for msg in reversed(request.messages):
        if msg.role == "user":
            if isinstance(msg.content, str):
                user_content = msg.content
            elif isinstance(msg.content, list):
                user_content = " ".join([
                    c.get("text", "") for c in msg.content 
                    if isinstance(c, dict) and c.get("type") == "text"
                ])
            break
    
    if not user_content:
        raise HTTPException(400, "No user message found")
    
    # Create/get agent
    session_id = str(uuid.uuid4())
    agent = MatrixAgent(session_id)
    await agent.init()
    
    try:
        response = await agent.chat(user_content, system_prompt)
        
        # Parse thinking blocks
        content_blocks = []
        thinking_match = re.search(r'<think>(.*?)</think>', response.content, re.DOTALL)
        
        if thinking_match:
            content_blocks.append({
                "type": "thinking",
                "thinking": thinking_match.group(1).strip()
            })
        
        # Main text content
        text_content = re.sub(r'<think>.*?</think>', '', response.content, flags=re.DOTALL).strip()
        if text_content:
            content_blocks.append({
                "type": "text",
                "text": text_content
            })
        
        result = {
            "id": f"msg_{response.id}",
            "type": "message",
            "role": "assistant",
            "content": content_blocks,
            "model": request.model,
            "stop_reason": "end_turn",
            "stop_sequence": None,
            "usage": {
                "input_tokens": len(user_content.split()) * 2,
                "output_tokens": len(response.content.split()) * 2,
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 0
            }
        }
        
        # Cache result
        prompt_cache.set(cache_key_messages, request.system or "", result)
        
        return result
        
    except Exception as e:
        raise HTTPException(500, str(e))


# ============== OPENAI COMPATIBLE API ==============

@app.post("/v1/chat/completions")
async def openai_chat_completions(
    request: OpenAIRequest,
    authorization: Optional[str] = Header(None)
):
    """
    OpenAI Chat Completions API compatible endpoint.
    Supports: tool use, streaming (basic).
    """
    start_time = time.time()
    
    # Build conversation
    system_prompt = ""
    user_content = ""
    
    for msg in request.messages:
        if msg.role == "system":
            system_prompt = msg.content or ""
        elif msg.role == "user":
            user_content = msg.content or ""
    
    if request.tools:
        tool_desc = "\n".join([
            f"- {t.function.get('name', '')}: {t.function.get('description', '')}" 
            for t in request.tools
        ])
        system_prompt += f"\n\nAvailable tools:\n{tool_desc}"
    
    if not user_content:
        raise HTTPException(400, "No user message found")
    
    # Create agent
    session_id = str(uuid.uuid4())
    agent = MatrixAgent(session_id)
    await agent.init()
    
    try:
        response = await agent.chat(user_content, system_prompt)
        
        # Remove thinking tags for OpenAI format
        clean_content = re.sub(r'<think>.*?</think>', '', response.content, flags=re.DOTALL).strip()
        
        result = {
            "id": f"chatcmpl-{response.id}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": request.model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": clean_content
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": len(user_content.split()) * 2,
                "completion_tokens": len(response.content.split()) * 2,
                "total_tokens": (len(user_content.split()) + len(response.content.split())) * 2
            }
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(500, str(e))


# ============== CODE ASSISTANT ENDPOINT ==============

class CodeRequest(BaseModel):
    code: str
    task: str = "explain"  # explain, review, refactor, complete, debug
    language: Optional[str] = None

@app.post("/v1/code")
@app.post("/anthropic/v1/code")
async def code_assistant(request: CodeRequest):
    """
    Specialized code understanding endpoint.
    Tasks: explain, review, refactor, complete, debug
    """
    task_prompts = {
        "explain": f"Explain this code in detail:\n```{request.language or ''}\n{request.code}\n```",
        "review": f"Review this code for bugs, security issues, and improvements:\n```{request.language or ''}\n{request.code}\n```",
        "refactor": f"Refactor this code for better readability and performance:\n```{request.language or ''}\n{request.code}\n```",
        "complete": f"Complete this code:\n```{request.language or ''}\n{request.code}\n```",
        "debug": f"Debug this code and identify issues:\n```{request.language or ''}\n{request.code}\n```"
    }
    
    prompt = task_prompts.get(request.task, task_prompts["explain"])
    
    session_id = str(uuid.uuid4())
    agent = MatrixAgent(session_id)
    await agent.init()
    
    try:
        response = await agent.chat(prompt)
        return {
            "task": request.task,
            "language": request.language,
            "response": response.content,
            "thinking": response.thinking
        }
    except Exception as e:
        raise HTTPException(500, str(e))


# ============== CACHE STATS ==============

@app.get("/v1/cache/stats")
async def cache_stats():
    """Get prompt cache statistics."""
    return prompt_cache.stats()


# ============== SESSIONS CRUD ==============

@app.post("/sessions", status_code=201)
async def create_session(body: SessionCreate = None):
    session_id = str(uuid.uuid4())
    name = body.name if body and body.name else None
    agent = MatrixAgent(session_id, name)
    await agent.init()
    agents[session_id] = agent
    return {"id": agent.session.id, "name": agent.session.name, "created_at": agent.session.created_at}

@app.get("/sessions")
async def list_sessions(skip: int = 0, limit: int = 100):
    sessions = [{"id": a.session.id, "name": a.session.name, "message_count": len(a.session.messages),
                 "created_at": a.session.created_at, "updated_at": a.session.updated_at} for a in agents.values()]
    return sessions[skip:skip+limit]

@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    if session_id not in agents:
        raise HTTPException(404, "Session not found")
    s = agents[session_id].session
    return {"id": s.id, "name": s.name, "message_count": len(s.messages), "created_at": s.created_at, "updated_at": s.updated_at}

@app.put("/sessions/{session_id}")
async def update_session(session_id: str, body: SessionUpdate):
    if session_id not in agents:
        raise HTTPException(404, "Session not found")
    agents[session_id].session.name = body.name
    agents[session_id].session.updated_at = datetime.utcnow().isoformat()
    return {"id": session_id, "name": body.name, "status": "updated"}

@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    if session_id not in agents:
        raise HTTPException(404, "Session not found")
    del agents[session_id]
    return {"id": session_id, "status": "deleted"}


# ============== MESSAGES CRUD ==============

@app.post("/sessions/{session_id}/messages")
async def create_message(session_id: str, body: MessageCreate):
    if session_id not in agents:
        raise HTTPException(404, "Session not found")
    try:
        msg = await agents[session_id].chat(body.content)
        return msg.to_dict()
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/sessions/{session_id}/messages")
async def list_messages(session_id: str, skip: int = 0, limit: int = 100):
    if session_id not in agents:
        raise HTTPException(404, "Session not found")
    messages = [m.to_dict() for m in agents[session_id].session.messages]
    return messages[skip:skip+limit]

@app.get("/sessions/{session_id}/messages/{message_id}")
async def get_message(session_id: str, message_id: str):
    if session_id not in agents:
        raise HTTPException(404, "Session not found")
    for m in agents[session_id].session.messages:
        if m.id == message_id:
            return m.to_dict()
    raise HTTPException(404, "Message not found")

@app.delete("/sessions/{session_id}/messages/{message_id}")
async def delete_message(session_id: str, message_id: str):
    if session_id not in agents:
        raise HTTPException(404, "Session not found")
    msgs = agents[session_id].session.messages
    for i, m in enumerate(msgs):
        if m.id == message_id:
            del msgs[i]
            return {"id": message_id, "status": "deleted"}
    raise HTTPException(404, "Message not found")

@app.delete("/sessions/{session_id}/messages")
async def clear_messages(session_id: str):
    if session_id not in agents:
        raise HTTPException(404, "Session not found")
    agents[session_id].session.messages = []
    return {"session_id": session_id, "status": "cleared"}


# ============== QUICK CHAT ==============

@app.post("/chat")
async def quick_chat(body: ChatRequest):
    session_id = body.session_id or str(uuid.uuid4())
    if session_id not in agents:
        agent = MatrixAgent(session_id)
        await agent.init()
        agents[session_id] = agent
    try:
        msg = await agents[session_id].chat(body.message)
        return {"session_id": session_id, "response": msg.content, "thinking": msg.thinking}
    except Exception as e:
        raise HTTPException(500, str(e))


# ============== CLI ==============

async def cli():
    print("\n🤖 MATRIX AGENT\nCapabilities: Code | PPT | Research | Multimodal | Browser\n")
    agent = MatrixAgent(str(uuid.uuid4()))
    await agent.init()
    while True:
        try:
            msg = input("You: ").strip()
            if msg.lower() == 'quit': break
            if not msg: continue
            resp = await agent.chat(msg)
            if '<think>' in resp.content:
                parts = re.split(r'(<think>.*?</think>)', resp.content, flags=re.DOTALL)
                for p in parts:
                    if p.startswith('<think>'):
                        print(f"\n💭 {re.sub(r'</?think>', '', p)}\n")
                    else:
                        print(p, end='')
            else:
                print(f"Agent: {resp.content}")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        asyncio.run(cli())
    else:
        import uvicorn
        port = int(os.environ.get("PORT", 7860))
        uvicorn.run(app, host="0.0.0.0", port=port)
