from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from enum import Enum
from .state_analyzer import StateAnalyzer, EmotionalState

class SessionState(Enum):
    INITIAL = "initial"
    ACTIVE = "active"
    NEEDS_GROUNDING = "needs_grounding"
    CRISIS = "crisis"
    CLOSING = "closing"

@dataclass
class TherapeuticMessage:
    content: str
    timestamp: datetime
    is_user: bool
    emotional_state: Optional[EmotionalState] = None

class TherapeuticSession:
    def __init__(self):
        self.messages: List[TherapeuticMessage] = []
        self.state: SessionState = SessionState.INITIAL
        self.grounding_exercises_offered: bool = False
        self.last_activity: datetime = datetime.now()
        self.state_analyzer = StateAnalyzer()
    
    def add_message(self, content: str, is_user: bool):
        emotional_state = self.state_analyzer.analyze_message(content) if is_user else None
        message = TherapeuticMessage(
            content=content,
            timestamp=datetime.now(),
            is_user=is_user,
            emotional_state=emotional_state
        )
        self.messages.append(message)
        self.last_activity = message.timestamp
        
    def evaluate_state(self) -> SessionState:
        if not self.messages:
            return SessionState.INITIAL
            
        recent_messages = self.messages[-3:]
        recent_user_messages = [msg for msg in recent_messages if msg.is_user]
        
        if any(msg.emotional_state and msg.emotional_state.risk_level > 0.7 for msg in recent_user_messages):
            return SessionState.CRISIS
        
        if any(msg.emotional_state and msg.emotional_state.intensity > 0.7 for msg in recent_user_messages):
            return SessionState.NEEDS_GROUNDING
        
        return SessionState.ACTIVE
    
    def needs_grounding_exercise(self) -> bool:
        if not self.messages or self.grounding_exercises_offered:
            return False
        
        recent_messages = [msg for msg in self.messages[-3:] if msg.is_user]
        return any(msg.emotional_state and msg.emotional_state.intensity > 0.7 for msg in recent_messages)
    
    def get_session_summary(self) -> dict:
        return {
            "duration": (datetime.now() - self.messages[0].timestamp).seconds if self.messages else 0,
            "message_count": len(self.messages),
            "user_message_count": sum(1 for msg in self.messages if msg.is_user),
            "current_state": self.state.value,
            "grounding_exercises_offered": self.grounding_exercises_offered,
            "average_emotional_intensity": sum(msg.emotional_state.intensity for msg in self.messages if msg.is_user and msg.emotional_state) / sum(1 for msg in self.messages if msg.is_user and msg.emotional_state) if any(msg.is_user and msg.emotional_state for msg in self.messages) else 0
        }