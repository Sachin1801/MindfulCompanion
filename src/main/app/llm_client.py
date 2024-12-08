import requests
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class LLMClient:
    def __init__(self, base_url: str = "http://localhost:1234"):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}

    def generate_response(self, messages: list) -> Dict[str, Any]:
        try:
            payload = {
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 500,
            }
            
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code != 200:
                logger.error(f"API Error: {response.text}")
                return {"error": "Failed to generate response"}

            result = response.json()
            return {
                "message": result["choices"][0]["message"]["content"],
                "usage": result.get("usage", {})
            }

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {"error": str(e)}