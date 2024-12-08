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