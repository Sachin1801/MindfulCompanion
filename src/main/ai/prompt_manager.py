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