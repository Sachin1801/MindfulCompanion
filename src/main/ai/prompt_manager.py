from typing import Dict, Optional, List
from .state_analyzer import EmotionalState

class TherapeuticPromptManager:
    def __init__(self):
        self.base_system_prompt = """You are MindfulCompanion, a supportive AI wellness companion focused on mental well-being. While you are not a replacement for professional mental health care, you provide:
1. Empathetic, non-judgmental listening
2. Evidence-based coping strategies
3. Mindfulness techniques
4. Emotional support and validation

Guidelines:
- Always maintain appropriate boundaries
- Be consistent and reliable in responses
- Use a warm, supportive tone
- Recognize signs of crisis and recommend professional help when needed
- Focus on validation and reflection before suggesting solutions
- Structure responses to be clear and calming
- Maintain context awareness for continuity of support

Safety Protocol:
- For any mentions of self-harm or severe distress, prioritize crisis resources
- Never attempt to diagnose or provide medical advice
- Be clear about your limitations as an AI companion"""

        # Theme-specific response strategies
        self.response_strategies = {
            "anxiety": {
                "coping_techniques": [
                    "deep breathing exercises",
                    "grounding techniques",
                    "progressive muscle relaxation"
                ],
                "validation_phrases": [
                    "anxiety can feel overwhelming",
                    "it's natural to feel anxious about uncertainty",
                    "many people experience similar feelings"
                ]
            },
            "depression": {
                "coping_techniques": [
                    "small achievable goals",
                    "gentle physical activity",
                    "connection with others"
                ],
                "validation_phrases": [
                    "depression can make everything feel harder",
                    "it's okay to take things one step at a time",
                    "your feelings are valid"
                ]
            },
            "stress": {
                "coping_techniques": [
                    "time management strategies",
                    "mindfulness exercises",
                    "stress reduction techniques"
                ],
                "validation_phrases": [
                    "stress can feel overwhelming",
                    "it's okay to feel pressured",
                    "managing multiple responsibilities is challenging"
                ]
            },
            "grief": {
                "coping_techniques": [
                    "honoring memories",
                    "self-compassion practices",
                    "expressing emotions"
                ],
                "validation_phrases": [
                    "grief is a unique journey",
                    "there's no timeline for healing",
                    "your feelings of loss are valid"
                ]
            }
        }

    def create_therapeutic_prompt(
        self, 
        user_message: str, 
        emotional_state: EmotionalState, 
        context: dict
    ) -> str:
        session_state = context.get('state', 'initial')
        current_topic = context.get('current_topic', None)
        
        # Get relevant strategies based on emotional state
        strategies = self.response_strategies.get(
            emotional_state.primary_emotion.lower(),
            self.response_strategies.get('stress')  # default fallback
        )

        prompt = f"""You are a supportive AI companion. Respond with ONLY a JSON object in this exact format:

{{
    "reflection": "I hear that you're feeling [emotion]",
    "validation": "It's normal to feel this way because [reason]",
    "support": "Let's try [specific suggestion]",
    "question": "What [follow-up question]?",
    "safety_note": ""
}}

User message: "{user_message}"

Remember:
1. ONLY output the JSON object
2. Keep it brief and warm
3. Be specific and actionable"""

        if emotional_state.risk_level > 0.7:
            prompt += """\nCRISIS PROTOCOL ACTIVATED:
- Express immediate concern for their safety
- Provide crisis resources (988 Crisis Line, 911)
- Encourage professional help
- Keep response focused on immediate safety"""
            
        return prompt

    def create_crisis_response(self) -> str:
        return """I'm very concerned about your safety right now. What you're going through is serious, and you deserve immediate support. While I'm here to listen, it's crucial to connect with professional help who can provide the support you need right now.

Crisis Resources Available 24/7:
- Crisis Text Line: 988
- Emergency Services: 911
- National Crisis Line: 1-800-273-8255

Would you be willing to reach out to one of these services? They are trained to help in situations exactly like this and want to support you."""

    def create_grounding_response(self) -> str:
        return """I notice you're experiencing intense emotions right now. Let's try a brief grounding exercise together:

Take a gentle breath and notice:
5 things you can see around you right now
4 things you can physically feel
3 things you can hear
2 things you can smell
1 thing you can taste

Would you like to try this together? We can take it one step at a time."""

    def create_fallback_response(self) -> str:
        return """I hear you, and what you're sharing is important. While I want to make sure I understand correctly before responding, know that I'm here to listen and support you. Could you tell me a bit more about what's on your mind right now?"""

    def _get_intensity_modifier(self, intensity: float) -> str:
        if intensity > 0.8:
            return "very intense"
        elif intensity > 0.6:
            return "significant"
        elif intensity > 0.4:
            return "moderate"
        else:
            return "mild"