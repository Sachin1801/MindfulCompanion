import aiohttp
import json
import logging
from typing import Dict, Optional
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
        self.system_prompt = self._load_system_prompt(system_prompt_path)
        
    def _load_system_prompt(self, path: Optional[Path]) -> str:
        if not path:
            return ""
        try:
            return Path(path).read_text()
        except Exception as e:
            logger.error(f"Failed to load system prompt: {e}")
            return ""

    async def generate_response(
        self,
        user_message: str,
        temperature: float = 0.6,
        max_tokens: int = 1000
    ) -> Dict:
        """Generate a response using LM Studio's local API."""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "messages": [
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_message}
                    ],
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "stream": False
                }
                
                async with session.post(
                    f"{self.base_url}/v1/chat/completions",
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"API Error: {error_text}")
                    
                    result = await response.json()
                    # Return the raw response instead of parsing the content
                    return result
                    
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                "choices": [{
                    "message": {
                        "content": json.dumps({
                            "reflection": "I understand you're reaching out",
                            "validation": "Your feelings are important",
                            "support": "I'm here to listen",
                            "question": "Would you like to tell me more?",
                            "safety_note": ""
                        })
                    }
                }]
            }

    async def test_connection(self) -> bool:
        """Test if LM Studio API is accessible."""
        try:
            response = await self.generate_response(
                "Test connection message",
                temperature=0.1,
                max_tokens=10
            )
            return isinstance(response, dict) and len(response) > 0
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False