import sys
sys.path.append('src/main')
import asyncio
import logging
import json
import re
from typing import Dict, List
from pathlib import Path
from ai.llm_client import LLMClient
from ai.prompt_manager import TherapeuticPromptManager
from ai.session_manager import TherapeuticSession, SessionState
from ai.state_analyzer import StateAnalyzer, EmotionalState

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
        
    async def _get_response(self, user_message: str, emotional_state: EmotionalState) -> Dict:
        """Generate therapeutic response based on comprehensive context"""
        try:
            context = self.session.get_session_context()
            
            # Generate response
            prompt = self.prompt_manager.create_therapeutic_prompt(
                user_message,
                emotional_state,
                context
            )
            
            response = await self.llm_client.generate_response(
                prompt,
                temperature=self._determine_temperature(emotional_state, context['state']),
                max_tokens=750
            )
            
            result = self._process_llm_response(response)
            
            # Verify response isn't a greeting if we're in an engaged conversation
            if context['state'] == 'engaged' and 'welcome' in result.get('reflection', '').lower():
                return {
                    "reflection": f"I understand that you're feeling {emotional_state.primary_emotion}",
                    "validation": "It's completely normal to feel this way",
                    "support": "Let's work through this together",
                    "question": "Can you tell me more about what's causing these feelings?",
                    "safety_note": ""
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Error in _get_response: {str(e)}")
            return self.prompt_manager.create_fallback_response()

    def _update_therapeutic_insights(self, response: Dict, emotional_state: EmotionalState):
        """Update session with therapeutic insights from response"""
        try:
            # Extract themes from response
            if 'reflection' in response:
                potential_themes = self._extract_themes(response['reflection'])
                self.session.themes.extend([theme for theme in potential_themes 
                                        if theme not in self.session.themes])
            
            # Track coping strategies
            if 'support' in response:
                strategies = self._extract_coping_strategies(response['support'])
                self.session.coping_strategies_discussed.extend(strategies)
        except Exception as e:
            logger.error(f"Error updating therapeutic insights: {str(e)}")

    def _extract_themes(self, text: str) -> List[str]:
        """Extract potential therapeutic themes from text"""
        # Simple implementation - can be enhanced with NLP
        common_themes = ['anxiety', 'depression', 'relationships', 'self-esteem', 
                        'grief', 'trauma', 'stress', 'sleep', 'anger']
        return [theme for theme in common_themes if theme.lower() in text.lower()]

    def _extract_coping_strategies(self, text: str) -> List[str]:
        """Extract mentioned coping strategies from text"""
        # Simple implementation - can be enhanced with NLP
        strategies = ['breathing', 'meditation', 'exercise', 'mindfulness', 
                     'grounding', 'self-care', 'therapy', 'journaling']
        return [strategy for strategy in strategies if strategy.lower() in text.lower()]

    async def process_message(self, user_message: str) -> str:
        try:
            # Validate input
            if not user_message or not user_message.strip():
                return "I didn't catch that. Could you please say something?"

            # Add message to session and analyze emotional state
            emotional_state = self.state_analyzer.analyze_message(user_message)
            self.session.add_message(user_message, is_user=True, emotional_state=emotional_state)
            
            result = await self._get_response(user_message, emotional_state)
            
            # Format the response for display
            if isinstance(result, dict):
                formatted_response = self._format_response_for_display(result)
            else:
                formatted_response = str(result)
                
            self.session.add_message(formatted_response, is_user=False)
            return formatted_response
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return "I apologize, but I'm having trouble processing your message. Could you try rephrasing it?"

    def _format_response_for_display(self, response_dict: Dict) -> str:
        """Convert response dictionary to natural language"""
        try:
            if not isinstance(response_dict, dict):
                return str(response_dict)
            
            parts = []
            
            # Build response naturally
            if response_dict.get("reflection"):
                parts.append(response_dict["reflection"].strip())
            
            if response_dict.get("validation"):
                validation = response_dict["validation"].strip()
                if not any(validation.lower().startswith(word) for word in ['and', 'also', 'additionally']):
                    parts.append(validation)
            
            if response_dict.get("support"):
                support = response_dict["support"].strip()
                if not any(support.lower().startswith(word) for word in ['and', 'also', 'additionally']):
                    parts.append(support)
            
            if response_dict.get("question"):
                question = response_dict["question"].strip()
                if not any(question.lower().startswith(word) for word in ['and', 'also', 'additionally']):
                    parts.append(question)
            
            if response_dict.get("safety_note"):
                safety = response_dict["safety_note"].strip()
                if safety:
                    parts.append(f"\nIMPORTANT: {safety}")
            
            # Join parts with proper spacing and punctuation
            response = '. '.join(filter(None, parts))
            response = response.replace('..', '.')  # Remove double periods
            response = re.sub(r'\s+', ' ', response).strip()  # Clean up whitespace
            
            # Ensure proper sentence capitalization
            sentences = response.split('. ')
            sentences = [s.strip().capitalize() for s in sentences if s.strip()]
            response = '. '.join(sentences)
            
            return response
            
        except Exception as e:
            logger.error(f"Error formatting response: {e}")
            return "I'm here to listen and support you. Would you like to share more?"

    async def run_interactive_session(self):
        welcome_message = {
            "reflection": "Welcome to MindfulCompanion",
            "validation": "I'm here to provide a supportive space for you",
            "support": "Feel free to share whatever is on your mind",
            "question": "How are you feeling today?",
            "safety_note": ""
        }
        print("\nMindfulCompanion:", self._format_response_for_display(welcome_message), "\n")
        
        while True:
            user_input = input("You: ").strip()
            if not user_input:
                continue
                
            if user_input.lower() == 'exit':
                farewell = {
                    "reflection": "Thank you for sharing with me today",
                    "validation": "Your willingness to open up is appreciated",
                    "support": "Remember that seeking support is a sign of strength",
                    "question": "",
                    "safety_note": ""
                }
                print("\nMindfulCompanion:", self._format_response_for_display(farewell))
                print("\nSession Summary:")
                print(json.dumps(self.session.get_session_summary(), indent=2))
                break
            
            response = await self.process_message(user_input)
            print("\nMindfulCompanion:", response, "\n")

    def _process_llm_response(self, response: str) -> Dict:
        """Helper method to process and clean LLM response"""
        try:
            # If response is already a dict with choices
            if isinstance(response, dict) and 'choices' in response:
                content = response['choices'][0]['message']['content']
            else:
                content = response

            # Clean up the content
            content = content.strip()
            
            # Try to find JSON structure
            try:
                # First attempt: direct JSON parsing
                return json.loads(content)
            except json.JSONDecodeError:
                # Second attempt: Find JSON-like structure and clean it
                json_pattern = r'\{[\s\S]*\}'
                matches = re.search(json_pattern, content)
                
                if matches:
                    json_str = matches.group(0)
                    
                    # Clean up the JSON string
                    json_str = re.sub(r'[\n\r]', '', json_str)  # Remove newlines
                    json_str = re.sub(r',\s*([\]}])', r'\1', json_str)  # Fix trailing commas
                    json_str = re.sub(r'([{,])\s*([^"{\s])', r'\1"\2', json_str)  # Add missing quotes to keys
                    json_str = re.sub(r'([^"}]),\s*([^"{\s])', r'\1,"\2', json_str)  # Add missing quotes to subsequent keys
                    
                    try:
                        return json.loads(json_str)
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse cleaned JSON: {e}")
                
                # If all parsing attempts fail, extract components manually
                reflection_match = re.search(r'"reflection":\s*"([^"]*)"', content)
                validation_match = re.search(r'"validation":\s*"([^"]*)"', content)
                support_match = re.search(r'"support":\s*"([^"]*)"', content)
                question_match = re.search(r'"question":\s*"([^"]*)"', content)
                safety_match = re.search(r'"safety_note":\s*"([^"]*)"', content)
                
                return {
                    "reflection": reflection_match.group(1) if reflection_match else "I understand your situation",
                    "validation": validation_match.group(1) if validation_match else "Your feelings are valid",
                    "support": support_match.group(1) if support_match else "Let's work through this together",
                    "question": question_match.group(1) if question_match else "Would you like to tell me more?",
                    "safety_note": safety_match.group(1) if safety_match else ""
                }
        
        except Exception as e:
            logger.error(f"Error processing LLM response: {str(e)}")
            # Return a failsafe response
            return {
                "reflection": "I hear what you're saying",
                "validation": "Your feelings matter",
                "support": "I'm here to support you",
                "question": "Can you tell me more about what's on your mind?",
                "safety_note": ""
            }

    def _determine_temperature(self, emotional_state: EmotionalState, session_state: str) -> float:
        """Determine the appropriate temperature based on emotional state and session state."""
        if session_state == 'crisis':
            return 0.2  # Most focused/consistent for crisis
        elif emotional_state.intensity > 0.7:
            return 0.3  # Very focused for high intensity
        elif session_state == 'initial':
            return 0.5  # Moderately creative for initial contact
        else:
            return 0.4  # Balanced for regular conversation

async def main():
    logger.info("Starting MindfulCompanion...")
    companion = MindfulCompanion()
    
    # Run the interactive session directly
    await companion.run_interactive_session()

if __name__ == "__main__":
    asyncio.run(main())