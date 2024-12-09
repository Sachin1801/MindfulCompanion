from pydantic import BaseModel
from typing import List, Optional

class UserProfile(BaseModel):
    name: str
    age_category: str
    emotions: List[str]
    therapy_status: str
    interaction_style: str
    stress_level: str
    goals: str

class ChatMessage(BaseModel):
    role: str
    content: str
    mood: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    mood: Optional[str] = None
    user_profile: Optional['UserProfile'] = None

class ChatResponse(BaseModel):
    message: str
    emotional_state: Optional[str] = None