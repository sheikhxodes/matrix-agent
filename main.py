"""
Matrix Agent - General Purpose AI with Interleaved Thinking
Preserves <think>...</think> content in conversation history
"""

import asyncio
import re
from dataclasses import dataclass, field
from typing import AsyncGenerator

from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

from agents.coordinator import coordinator_agent


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


async def main():
    print("\n\U0001f916 MATRIX AGENT\nCapabilities: Code | PPT | Research | Multimodal\n")
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
    asyncio.run(main())
