"""
Matrix Agent - General Purpose AI with Interleaved Thinking
FastAPI Application with Full CRUD Endpoints
"""

import asyncio
import os
import re
import uuid
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
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
    
    async def chat(self, content: str) -> Message:
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
    description="General-purpose AI agent with multi-step planning",
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


# ============== HEALTH & INFO ==============

@app.get("/")
async def root():
    return {
        "name": "Matrix Agent",
        "version": "0.1.0",
        "capabilities": ["Code", "PPT", "Research", "Multimodal"],
        "status": "ready"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


# ============== SESSIONS CRUD ==============

# CREATE
@app.post("/sessions", status_code=201)
async def create_session(body: SessionCreate = None):
    """Create a new session."""
    session_id = str(uuid.uuid4())
    name = body.name if body and body.name else None
    agent = MatrixAgent(session_id, name)
    await agent.init()
    agents[session_id] = agent
    return {
        "id": agent.session.id,
        "name": agent.session.name,
        "created_at": agent.session.created_at
    }

# READ ALL
@app.get("/sessions")
async def list_sessions(skip: int = 0, limit: int = 100):
    """List all sessions."""
    sessions = [{
        "id": a.session.id,
        "name": a.session.name,
        "message_count": len(a.session.messages),
        "created_at": a.session.created_at,
        "updated_at": a.session.updated_at
    } for a in agents.values()]
    return sessions[skip:skip+limit]

# READ ONE
@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """Get session details."""
    if session_id not in agents:
        raise HTTPException(404, "Session not found")
    s = agents[session_id].session
    return {
        "id": s.id,
        "name": s.name,
        "message_count": len(s.messages),
        "created_at": s.created_at,
        "updated_at": s.updated_at
    }

# UPDATE
@app.put("/sessions/{session_id}")
async def update_session(session_id: str, body: SessionUpdate):
    """Update session name."""
    if session_id not in agents:
        raise HTTPException(404, "Session not found")
    agents[session_id].session.name = body.name
    agents[session_id].session.updated_at = datetime.utcnow().isoformat()
    return {"id": session_id, "name": body.name, "status": "updated"}

# DELETE
@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session."""
    if session_id not in agents:
        raise HTTPException(404, "Session not found")
    del agents[session_id]
    return {"id": session_id, "status": "deleted"}


# ============== MESSAGES CRUD ==============

# CREATE (chat)
@app.post("/sessions/{session_id}/messages")
async def create_message(session_id: str, body: MessageCreate):
    """Send a message and get response."""
    if session_id not in agents:
        raise HTTPException(404, "Session not found")
    try:
        msg = await agents[session_id].chat(body.content)
        return msg.to_dict()
    except Exception as e:
        raise HTTPException(500, str(e))

# READ ALL
@app.get("/sessions/{session_id}/messages")
async def list_messages(session_id: str, skip: int = 0, limit: int = 100):
    """List all messages in session."""
    if session_id not in agents:
        raise HTTPException(404, "Session not found")
    messages = [m.to_dict() for m in agents[session_id].session.messages]
    return messages[skip:skip+limit]

# READ ONE
@app.get("/sessions/{session_id}/messages/{message_id}")
async def get_message(session_id: str, message_id: str):
    """Get a specific message."""
    if session_id not in agents:
        raise HTTPException(404, "Session not found")
    for m in agents[session_id].session.messages:
        if m.id == message_id:
            return m.to_dict()
    raise HTTPException(404, "Message not found")

# DELETE ONE
@app.delete("/sessions/{session_id}/messages/{message_id}")
async def delete_message(session_id: str, message_id: str):
    """Delete a message."""
    if session_id not in agents:
        raise HTTPException(404, "Session not found")
    msgs = agents[session_id].session.messages
    for i, m in enumerate(msgs):
        if m.id == message_id:
            del msgs[i]
            return {"id": message_id, "status": "deleted"}
    raise HTTPException(404, "Message not found")

# DELETE ALL
@app.delete("/sessions/{session_id}/messages")
async def clear_messages(session_id: str):
    """Clear all messages in session."""
    if session_id not in agents:
        raise HTTPException(404, "Session not found")
    agents[session_id].session.messages = []
    return {"session_id": session_id, "status": "cleared"}


# ============== QUICK CHAT ==============

@app.post("/chat")
async def quick_chat(body: ChatRequest):
    """Quick chat - creates session if needed."""
    session_id = body.session_id or str(uuid.uuid4())
    
    if session_id not in agents:
        agent = MatrixAgent(session_id)
        await agent.init()
        agents[session_id] = agent
    
    try:
        msg = await agents[session_id].chat(body.message)
        return {
            "session_id": session_id,
            "response": msg.content,
            "thinking": msg.thinking
        }
    except Exception as e:
        raise HTTPException(500, str(e))


# ============== CLI ==============

async def cli():
    print("\n🤖 MATRIX AGENT\nCapabilities: Code | PPT | Research | Multimodal\n")
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
