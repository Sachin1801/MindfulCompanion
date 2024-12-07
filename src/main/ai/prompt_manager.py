from typing import Dict, Optional

class TherapeuticPromptManager:
    def __init__(self):
        self.system_prompt = """You are a supportive mental wellness companion. Respond with empathy and structure.
Always provide responses in the following JSON format:
{
    "reflection": "Mirror the user's emotions",
    "validation": "Validate their experience",
    "support": "Offer gentle support or coping strategy",
    "question": "Optional follow-up question for exploration",
    "safety_note": "Include if crisis indicators detected"
}"""

    def create_therapeutic_prompt(self, user_message: str) -> str:
        return f"""Analyze the following message with empathy and respond with a JSON object containing these exact keys:

User message: {user_message}

Required JSON format:
{{
    "reflection": "Mirror the user's emotions",
    "validation": "Validate their experience",
    "support": "Offer gentle support",
    "question": "Follow-up question",
    "safety_concern_flag": false
}}

Return ONLY the JSON object, no additional text."""

    def create_crisis_response(self) -> Dict:
        return {
            "reflection": "I hear that you're in significant pain right now",
            "validation": "What you're going through is serious and you deserve support",
            "support": "While I'm here to listen, it's important to get professional help",
            "safety_note": "Please reach out to crisis support: Emergency Services (911) or Crisis Text Line (988)"
        }

    def check_crisis_indicators(self, message: str) -> bool:
        crisis_keywords = [
            "suicide", "kill myself", "end it all", "want to die",
            "hurt myself", "self-harm", "no reason to live"
        ]
        return any(keyword in message.lower() for keyword in crisis_keywords)