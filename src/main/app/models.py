from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    message: str
    emotional_state: Optional[str] = None