#main.pyimport sys
sys.path.append('src/main')
import asyncio
import logging
from typing import Dict
from ai.llm_client import LLMClient
from ai.prompt_manager import TherapeuticPromptManager
from ai.session_manager import TherapeuticSession, SessionState
from ai.state_analyzer import StateAnalyzer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MindfulCompanion:
    def __init__(self):
        self.llm_client = LLMClient()
        self.prompt_manager = TherapeuticPromptManager()
        self.session = TherapeuticSession()
        self.state_analyzer = StateAnalyzer()
        
    async def process_message(self, user_message: str) -> Dict:
        try:
            # Add message to session and analyze emotional state
            self.session.add_message(user_message, is_user=True)
            emotional_state = self.state_analyzer.analyze_message(user_message)
            
            # Evaluate session state
            session_state = self.session.evaluate_state()
            
            if session_state == SessionState.CRISIS:
                return self.prompt_manager.create_crisis_response(emotional_state)
            
            if session_state == SessionState.NEEDS_GROUNDING:
                self.session.grounding_exercises_offered = True
                return self.prompt_manager.create_grounding_response()
            
            # Generate therapeutic prompt
            prompt = self.prompt_manager.create_therapeutic_prompt(user_message)
            
            # Get LLM response
            response = await self.llm_client.generate_response(
                prompt,
                temperature=0.5,
                max_tokens=500
            )
            
            logger.debug(f"Raw LLM response: {response}")
            
            # Add AI response to session
            self.session.add_message(str(response), is_user=False)
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return self.prompt_manager.create_fallback_response()

    async def run_interactive_session(self):
        print("Welcome to MindfulCompanion. Type 'exit' to end the session.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Thank you for using MindfulCompanion. Take care!")
                break
            
            response = await self.process_message(user_input)
            print("\nMindfulCompanion:")
            for key, value in response.items():
                if value:  # Only print non-empty values
                    print(f"{key.capitalize()}: {value}")
            print()  # Add a blank line for readability
            
            if self.session.state == SessionState.CRISIS:
                print("Crisis detected. Please seek professional help immediately.")
                break

async def main():
    logger.info("Starting MindfulCompanion...")
    companion = MindfulCompanion()
    await companion.run_interactive_session()

if __name__ == "__main__":
    asyncio.run(main())

#llm_client.py
import aiohttp
import logging
from typing import Optional, Dict
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(
        self,
        base_url: str = "http://127.0.0.1:1234",
        system_prompt_path: Optional[Path] = None
    ):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
        
    async def generate_response(
        self,
        user_message: str,
        temperature: float = 0.5,
        max_tokens: int = 300
    ) -> Dict:
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "messages": [
                        {"role": "system", "content": "You are a supportive mental wellness companion. Keep responses concise and in JSON format."},
                        {"role": "user", "content": user_message}
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": False,
                    "stop": ["}"]
                }
                
                async with session.post(
                    f"{self.base_url}/v1/chat/completion",
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"API Error: {error_text}")
                    
                    result = await response.json()
                    content = result['choices'][0]['message']['content']
                    
                    # Clean up response
                    content = content.strip()
                    if not content.endswith('}'):
                        content += '}'
                    
                    try:
                        return json.loads(content)
                    except json.JSONDecodeError:
                        # Extract JSON from response if possible
                        import re
                        json_match = re.search(r'(\{.*\})', content.replace('\n', ' '), re.DOTALL)
                        if json_match:
                            return json.loads(json_match.group(1))
                        raise
                        
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "reflection": "I hear you",
                "support": "I'm here to listen",
                "action": "Would you like to tell me more?"
            }
        
#prompt_manager.py
from typing import Dict, Optional
from .state_analyzer import StateAnalyzer, EmotionalState

class TherapeuticPromptManager:
    def __init__(self):
        self.state_analyzer = StateAnalyzer()
        self.system_prompt = """You are a supportive mental wellness companion. Keep responses concise and empathetic.
Your response must be in valid JSON format with these keys only:
{
    "reflection": "brief emotional reflection",
    "support": "brief supportive statement",
    "action": "suggested coping strategy if needed"
}"""

    def create_therapeutic_prompt(self, user_message: str) -> str:
        emotional_state = self.state_analyzer.analyze_message(user_message)
        
        return f"""Respond to: "{user_message}"

Return only a JSON object with these exact keys:
{{
    "reflection": "brief emotional reflection",
    "support": "brief supportive statement",
    "action": "suggested coping strategy if needed"
}}

Keep each response element under 50 words. Focus on {emotional_state.primary_emotion}."""

    def create_crisis_response(self, emotional_state: Optional[EmotionalState] = None) -> Dict:
        return {
            "reflection": "I hear you're in pain",
            "support": "Your life has value. Professional help is available.",
            "action": "Please call 988 for immediate support, or 911 if in immediate danger."
        }

    def create_grounding_response(self) -> Dict:
        return {
            "reflection": "I notice strong emotions",
            "support": "Let's take a moment to ground ourselves",
            "action": "Try this: Name 5 things you can see right now."
        }

    def create_fallback_response(self) -> Dict:
        return {
            "reflection": "I hear you",
            "support": "I'm here to listen",
            "action": "Would you like to tell me more?"
        }
    
#session_manager.py
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
    
#state_analyzer.py
from typing import Dict, List, Optional
import re
from dataclasses import dataclass
from datetime import datetime

@dataclass
class EmotionalState:
    primary_emotion: str
    intensity: float  # 0-1 scale
    risk_level: float  # 0-1 scale
    timestamp: datetime

class StateAnalyzer:
    def __init__(self):
        self.emotion_patterns = {
            'depression': [
                r'worthless', r'nothing but', r'never get around',
                r'barely sleep', r'don\'t deserve', r'given up'
            ],
            'anxiety': [
                r'can\'t stop', r'constantly', r'overwhelming',
                r'never ends', r'worried sick', r'panic'
            ],
            'crisis': [
                r'suicide', r'kill myself', r'better off dead',
                r'end it all', r'no point living'
            ]
        }
        
        self.intensity_modifiers = [
            (r'very|really|extremely|completely', 0.3),
            (r'always|never|constantly', 0.2),
            (r'sometimes|occasionally', -0.1),
            (r'maybe|perhaps', -0.2)
        ]
        
    def analyze_message(self, message: str) -> EmotionalState:
        message = message.lower()
        primary_emotion = self._detect_primary_emotion(message)
        intensity = self._calculate_intensity(message)
        risk_level = self._assess_risk(message, primary_emotion, intensity)
        
        return EmotionalState(
            primary_emotion=primary_emotion,
            intensity=intensity,
            risk_level=risk_level,
            timestamp=datetime.now()
        )
    
    def _detect_primary_emotion(self, message: str) -> str:
        emotion_scores = {}
        
        for emotion, patterns in self.emotion_patterns.items():
            score = sum(len(re.findall(pattern, message)) for pattern in patterns)
            emotion_scores[emotion] = score
            
        return max(emotion_scores.items(), key=lambda x: x[1])[0]
    
    def _calculate_intensity(self, message: str) -> float:
        base_intensity = 0.5
        
        for pattern, modifier in self.intensity_modifiers:
            if re.search(pattern, message):
                base_intensity = min(1.0, max(0.0, base_intensity + modifier))
                
        return base_intensity
    
    def _assess_risk(self, message: str, emotion: str, intensity: float) -> float:
        risk_level = 0.0
        
        # Base risk on emotion type
        if emotion == 'crisis':
            risk_level = 0.8
        elif emotion == 'depression':
            risk_level = 0.4
        elif emotion == 'anxiety':
            risk_level = 0.3
            
        # Adjust risk based on intensity
        risk_level = min(1.0, risk_level + (intensity * 0.2))
        
        # Check for immediate risk patterns
        immediate_risk_patterns = [
            r'right now', r'tonight', r'plan to',
            r'going to', r'decided to'
        ]
        
        if any(re.search(pattern, message) for pattern in immediate_risk_patterns):
            risk_level = min(1.0, risk_level + 0.3)
            
        return risk_level

    def get_response_type(self, state: EmotionalState) -> str:
        if state.risk_level > 0.7:
            return 'crisis'
        elif state.risk_level > 0.5:
            return 'urgent'
        elif state.intensity > 0.7:
            return 'grounding'
        else:
            return 'supportive'