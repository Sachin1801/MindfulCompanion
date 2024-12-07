import sys
sys.path.append('src/main')
import asyncio
import logging
import json
from typing import Dict
from pathlib import Path
from ai.llm_client import LLMClient
from ai.prompt_manager import TherapeuticPromptManager
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
class MindfulCompanion:
    def __init__(self):
        self.llm_client = LLMClient()
        self.prompt_manager = TherapeuticPromptManager()
        
    async def process_message(self, user_message: str) -> Dict:
        try:
            # Check for crisis indicators
            if self.prompt_manager.check_crisis_indicators(user_message):
                return self.prompt_manager.create_crisis_response()
            
            # Generate therapeutic prompt
            prompt = self.prompt_manager.create_therapeutic_prompt(user_message)
            
            # Get LLM response
            response = await self.llm_client.generate_response(
                prompt,
                temperature=0.5,
                max_tokens=500
            )
            
            # Add debug logging
            logger.debug(f"Raw LLM response: {response}")
            
            # Clean and extract JSON
            try:
                # First attempt: direct parsing
                result = json.loads(response)
            except json.JSONDecodeError:
                # Second attempt: try to extract JSON from the response
                import re
                json_match = re.search(r'(\{.*\})', response.replace('\n', ' '), re.DOTALL)
                if json_match:
                    cleaned_json = json_match.group(1)
                    result = json.loads(cleaned_json)
                else:
                    raise
                    
            return result
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response: {str(e)}\nResponse: {response}")
            return {
                "reflection": "I understand you're sharing something important",
                "validation": "Your feelings matter",
                "support": "I'm here to listen and support you",
                "question": "Would you like to tell me more about what's on your mind?"
            }
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return {"error": "I apologize, but I'm having trouble processing your message"}

async def main():
    logger.info("Starting MindfulCompanion...")
    companion = MindfulCompanion()
    
    # Test messages
    test_messages = [
        "I've been feeling really overwhelmed with work lately",
        # "I'm having trouble sleeping and can't stop worrying",
        # "Everything feels really heavy and I'm struggling to cope"
    ]
    
    for message in test_messages:
        logger.info(f"\nUser: {message}")
        response = await companion.process_message(message)
        logger.info(f"Assistant: {json.dumps(response, indent=2)}")

if __name__ == "__main__":
    asyncio.run(main())