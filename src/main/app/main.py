from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import ChatRequest, ChatResponse
from .llm_client import LLMClient
from .prompt_helper import PromptHelper
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MindfulCompanion API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
llm_client = LLMClient()
prompt_helper = PromptHelper()

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Format conversation with system prompt
        messages = prompt_helper.format_conversation(request.message)
        
        # Generate response
        response = llm_client.generate_response(messages)
        
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
            
        return ChatResponse(
            message=response["message"],
            emotional_state="supportive"  # This can be enhanced with actual emotion detection
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)