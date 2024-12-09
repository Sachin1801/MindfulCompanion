from typing import List, Optional
from .models import UserProfile, ChatMessage
from .safety_monitor import SafetyMonitor

class PromptHelper:
    def __init__(self):
        self.safety_monitor = SafetyMonitor()

    def get_system_prompt(self, user_profile: Optional[UserProfile] = None) -> str:
        base_prompt = """You are MindfulCompanion, a supportive AI wellness companion. Follow these guidelines:

1. Therapeutic Approach:
   - Use active listening techniques
   - Practice reflective responses
   - Validate emotions before suggesting solutions
   - Maintain professional boundaries

2. Response Structure:
   - Begin with emotional reflection
   - Validate their experience
   - Offer gentle exploration
   - Suggest coping strategies when appropriate

3. Safety Protocols:
   - Recognize crisis signals
   - Provide appropriate resources
   - Maintain consistent support"""

        if user_profile:
            context = f"""
Current User Context:
- Age Group: {user_profile.age_category}
- Key Concerns: {', '.join(user_profile.emotions)}
- Therapy Status: {user_profile.therapy_status}
- Communication: {user_profile.interaction_style}
- Goals: {user_profile.goals}

Adapt your therapeutic approach accordingly. They prefer {user_profile.interaction_style} communication."""
            return base_prompt + context
        return base_prompt

    def format_conversation(self, message: str, mood: Optional[str], history: List[ChatMessage], user_profile: Optional[UserProfile]) -> list:
        # First check for safety concerns
        safety_check = self.safety_monitor.analyze_message(message)
        
        if safety_check['risk_level'] in ['high', 'severe']:
            # Modify system prompt for crisis response
            crisis_prompt = self._create_crisis_prompt(safety_check)
            return [
                {"role": "system", "content": crisis_prompt},
                {"role": "user", "content": message}
            ]

        # Normal conversation flow
        messages = [{"role": "system", "content": self.get_system_prompt(user_profile)}]
        
        # Add relevant history (last 5 messages)
        for msg in history[-5:]:
            messages.append({"role": msg.role, "content": msg.content})
        
        # Add current message with mood if provided
        current_message = message
        if mood:
            current_message = f"[Current Mood: {mood}] {message}"
            
        messages.append({"role": "user", "content": current_message})
        return messages

    def _create_crisis_prompt(self, safety_check: dict) -> str:
        return f"""IMPORTANT: Crisis situation detected. Respond with:
1. Express immediate concern for safety
2. Validate feelings with empathy
3. Share these crisis resources: {', '.join(safety_check['response']['resources'])}
4. Encourage immediate professional help
5. Keep response clear and direct

Current Risk Level: {safety_check['risk_level']}
Required Actions: {safety_check['response'].get('actions', [])}"""