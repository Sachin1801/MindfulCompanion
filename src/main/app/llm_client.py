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
                "temperature": 0.5,
                "max_tokens": 500,
            }
            
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            
            result = response.json()
            if not result.get("choices"):
                raise ValueError("No choices in response")
            
            return {
                "message": result["choices"][0]["message"]["content"],
                "usage": result.get("usage", {}),
                "status": "success"
            }

        except requests.Timeout:
            logger.error("Request timed out")
            return {"error": "Request timed out", "status": "timeout"}
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return {"error": str(e), "status": "request_failed"}
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {"error": str(e), "status": "error"}