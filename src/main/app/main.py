from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .models import ChatRequest, ChatResponse, UserProfile, ChatMessage
from .llm_client import LLMClient
from .prompt_helper import PromptHelper
from .database import Database
import logging
from typing import Optional
from .session_analyzer import SessionAnalyzer
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="MindfulCompanion API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
db = Database()
llm_client = LLMClient()
prompt_helper = PromptHelper()
session_analyzer = SessionAnalyzer()

# Dependency to get current user (in a real app, this would use authentication)
async def get_current_user_id() -> int:
    return 1  # Placeholder: In production, get this from auth token

@app.post("/profile")
async def create_profile(profile: UserProfile, user_id: int = Depends(get_current_user_id)):
    try:
        user_id = db.save_user_profile(profile)
        return {"user_id": user_id, "message": "Profile created successfully"}
    except Exception as e:
        logger.error(f"Error creating profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    user_id: int = Depends(get_current_user_id)
):
    try:
        # Get user profile and chat history
        profile = db.get_user_profile(user_id)
        history = db.get_chat_history(user_id)
        
        # Format conversation with context
        messages = prompt_helper.format_conversation(
            message=request.message,
            mood=request.mood,
            history=history,
            user_profile=profile
        )
        
        # Generate response
        response = llm_client.generate_response(messages)
        
        # Save the interaction
        db.save_chat_message(user_id, ChatMessage(
            role="user",
            content=request.message,
            mood=request.mood
        ))
        
        db.save_chat_message(user_id, ChatMessage(
            role="assistant",
            content=response["message"]
        ))
        
        return ChatResponse(
            message=response["message"],
            emotional_state="supportive"  # This could be enhanced with actual emotion detection
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
async def get_history(user_id: int = Depends(get_current_user_id)):
    try:
        history = db.get_chat_history(user_id)
        return {"history": history}
    except Exception as e:
        logger.error(f"Error getting history: {e}")
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/analysis/mood")
async def get_mood_analysis(user_id: int = Depends(get_current_user_id)):
    try:
        # Get chat history
        history = db.get_chat_history(user_id)
        
        # Analyze moods
        analysis = session_analyzer.analyze_mood_trends(history)
        
        return {
            "analysis": analysis,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error analyzing moods: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset")
async def reset_profile(user_id: int = Depends(get_current_user_id)):
    try:
        # Implement profile reset logic
        pass
    except Exception as e:
        logger.error(f"Error resetting profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, user_id: int = Depends(get_current_user_id)):
    try:
        # Check for crisis content
        safety_check = prompt_helper.safety_monitor.analyze_message(request.message)
        
        # Log crisis detection for monitoring
        if safety_check['risk_level'] in ['high', 'severe']:
            logger.warning(f"Crisis detected - User ID: {user_id}, Risk Level: {safety_check['risk_level']}")
            # Could add additional crisis protocols here
        
        # Continue with normal processing but with crisis awareness
        messages = prompt_helper.format_conversation(
            message=request.message,
            mood=request.mood,
            history=db.get_chat_history(user_id),
            user_profile=db.get_user_profile(user_id)
        )
        
        response = llm_client.generate_response(messages)
        
        return ChatResponse(
            message=response["message"],
            emotional_state=safety_check['risk_level'],
            crisis_resources=safety_check.get('response', {}).get('resources', []) if safety_check['risk_level'] != 'normal' else None
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)