"""
Matrix Agent - General Purpose AI with Interleaved Thinking
FastAPI + CLI Application
"""

import asyncio
import os
import re
from dataclasses import dataclass, field
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from agents.coordinator import coordinator_agent


# ============== DATA CLASSES ==============

@dataclass
class Message:
    role: str
    content: str
    thinking: str = ""
    
    def to_dict(self) -> dict:
        return {"role": self.role, "content": self.content}
    
    @classmethod
    def from_response(cls, content: str) -> "Message":
        thinking = ""
        match = re.search(r'<think>(.*?)</think>', content, re.DOTALL)
        if match:
            thinking = match.group(1).strip()
        return cls(role="assistant", content=content, thinking=thinking)


@dataclass
class ConversationHistory:
    messages: list[Message] = field(default_factory=list)
    
    def add_user(self, content: str):
        self.messages.append(Message(role="user", content=content))
    
    def add_assistant(self, content: str):
        self.messages.append(Message.from_response(content))
    
    def to_list(self) -> list[dict]:
        return [m.to_dict() for m in self.messages]


# ============== MATRIX AGENT CLASS ==============

class MatrixAgent:
    def __init__(self):
        self.agent = coordinator_agent
        self.session_service = InMemorySessionService()
        self.history = ConversationHistory()
        self.session = None
        self.runner = None
    
    async def init(self, user_id: str = "user"):
        self.session = await self.session_service.create_session(
            app_name="matrix_agent", user_id=user_id
        )
        self.runner = Runner(agent=self.agent, session_service=self.session_service)
        return self
    
    async def chat(self, message: str) -> str:
        if not self.runner:
            await self.init()
        self.history.add_user(message)
        response = ""
        async for event in self.runner.run_async(
            session_id=self.session.id, user_id="user", new_message=message
        ):
            if hasattr(event, 'content') and event.content:
                response += event.content
        self.history.add_assistant(response)
        return response


# ============== FASTAPI APP ==============

app = FastAPI(
    title="Matrix Agent API",
    description="General-purpose AI agent with multi-step planning and interleaved thinking",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Session storage
agents: dict[str, MatrixAgent] = {}


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    response: str
    thinking: str = ""
    session_id: str


@app.get("/")
async def root():
    return {
        "name": "Matrix Agent",
        "version": "0.1.0",
        "capabilities": ["Code", "PPT", "Research", "Multimodal"],
        "status": "ready"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with Matrix Agent. Thinking is preserved in session history."""
    try:
        if request.session_id not in agents:
            agents[request.session_id] = await MatrixAgent().init(request.session_id)
        
        agent = agents[request.session_id]
        response = await agent.chat(request.message)
        
        # Extract thinking for response
        thinking = ""
        think_match = re.search(r'<think>(.*?)</think>', response, re.DOTALL)
        if think_match:
            thinking = think_match.group(1).strip()
        
        return ChatResponse(
            response=response,
            thinking=thinking,
            session_id=request.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history/{session_id}")
async def get_history(session_id: str):
    """Get conversation history with thinking preserved."""
    if session_id not in agents:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"history": agents[session_id].history.to_list()}


@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session."""
    if session_id in agents:
        del agents[session_id]
        return {"status": "deleted", "session_id": session_id}
    raise HTTPException(status_code=404, detail="Session not found")


# ============== CLI MODE ==============

async def cli_main():
    print("\n\U0001f916 MATRIX AGENT")
    print("Capabilities: Code | PPT | Research | Multimodal\n")
    agent = await MatrixAgent().init()
    while True:
        try:
            msg = input("You: ").strip()
            if msg.lower() == 'quit': break
            if not msg: continue
            resp = await agent.chat(msg)
            if '<think>' in resp:
                parts = re.split(r'(<think>.*?</think>)', resp, flags=re.DOTALL)
                for p in parts:
                    if p.startswith('<think>'):
                        print(f"\n\U0001f4ad {re.sub(r'</?think>', '', p)}\n")
                    else:
                        print(p, end='')
            else:
                print(f"Agent: {resp}")
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        asyncio.run(cli_main())
    else:
        import uvicorn
        port = int(os.environ.get("PORT", 8000))
        uvicorn.run(app, host="0.0.0.0", port=port)
