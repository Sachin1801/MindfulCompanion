from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum
from .state_analyzer import StateAnalyzer, EmotionalState

class SessionState(Enum):
    INITIAL = "initial"
    ENGAGED = "engaged"
    CRISIS = "crisis"
    CLOSING = "closing"

class TherapeuticSession:
    def __init__(self):
        self.messages: List[Dict] = []
        self.state: SessionState = SessionState.INITIAL
        self.current_topic: Optional[str] = None
        self.themes: List[str] = []
        self.last_activity = datetime.now()
        self.grounding_exercises_offered = False
        self.coping_strategies_discussed: List[str] = []
        
    def add_message(self, content: str, is_user: bool, emotional_state: Optional[EmotionalState] = None):
        message = {
            'content': content,
            'is_user': is_user,
            'timestamp': datetime.now(),
            'emotional_state': emotional_state
        }
        self.messages.append(message)
        self.last_activity = message['timestamp']
        
        if len(self.messages) > 2:
            self.state = SessionState.ENGAGED

    def evaluate_state(self) -> SessionState:
        if not self.messages:
            return SessionState.INITIAL
            
        recent_messages = self.messages[-3:]
        recent_user_messages = [msg for msg in recent_messages if msg['is_user']]
        
        if any(msg['emotional_state'] and msg['emotional_state'].risk_level > 0.7 
               for msg in recent_user_messages):
            return SessionState.CRISIS
        
        if any(msg['emotional_state'] and msg['emotional_state'].intensity > 0.7 
               for msg in recent_user_messages):
            return SessionState.ENGAGED
        
        return self.state

    def get_session_summary(self) -> dict:
        if not self.messages:
            return {
                "duration": 0,
                "message_count": 0,
                "user_message_count": 0,
                "current_state": self.state.value,
                "grounding_exercises_offered": self.grounding_exercises_offered,
                "themes_discussed": self.themes,
                "coping_strategies_discussed": self.coping_strategies_discussed,
                "average_emotional_intensity": 0
            }
            
        duration = (datetime.now() - self.messages[0]['timestamp']).seconds
        user_messages = [msg for msg in self.messages if msg['is_user']]
        
        emotional_intensities = [
            msg['emotional_state'].intensity 
            for msg in user_messages 
            if msg['emotional_state']
        ]
        
        avg_intensity = (
            sum(emotional_intensities) / len(emotional_intensities)
            if emotional_intensities else 0
        )
        
        return {
            "duration": duration,
            "message_count": len(self.messages),
            "user_message_count": len(user_messages),
            "current_state": self.state.value,
            "grounding_exercises_offered": self.grounding_exercises_offered,
            "themes_discussed": self.themes,
            "coping_strategies_discussed": self.coping_strategies_discussed,
            "average_emotional_intensity": avg_intensity
        }

    def get_session_context(self) -> Dict:
        if not self.messages:
            return {
                'state': SessionState.INITIAL.value,
                'summary': "Initial session",
                'current_topic': None
            }

        recent_messages = self.messages[-3:]
        topics = []
        for msg in recent_messages:
            if msg['is_user'] and msg['emotional_state']:
                topics.append(msg['emotional_state'].primary_emotion)

        return {
            'state': self.state.value,
            'summary': self._generate_summary(recent_messages),
            'current_topic': topics[-1] if topics else None
        }

    def _generate_summary(self, messages: List[Dict]) -> str:
        if not messages:
            return "Initial session"
            
        user_messages = [msg for msg in messages if msg['is_user']]
        if not user_messages:
            return "Initial session"
            
        latest_msg = user_messages[-1]
        if latest_msg['emotional_state']:
            return f"User expressing {latest_msg['emotional_state'].primary_emotion}"
        return "Ongoing conversation"