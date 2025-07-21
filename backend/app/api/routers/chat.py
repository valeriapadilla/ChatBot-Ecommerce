import logging
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat.chat_service import ChatService
from app.services.chat.chat_history_service import ChatHistoryService
from app.interfaces.chat_interface import ChatServiceInterface
from app.exceptions.chat_exceptions import ChatValidationException, ChatProcessingException
from app.api.deps import get_db, get_current_active_user
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

def get_chat_service() -> ChatServiceInterface:
    return ChatService()

def get_history_service(db: Session) -> ChatHistoryService:
    return ChatHistoryService(db)

def handle_chat_exceptions(func):
    """Decorator to handle common chat exceptions."""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ChatValidationException as e:
            logger.warning("Validation error: %s", str(e))
            raise HTTPException(status_code=400, detail=str(e))
        except ChatProcessingException as e:
            logger.error("Processing error: %s", str(e))
            raise HTTPException(status_code=500, detail="Error processing chat request")
        except Exception as e:
            logger.error("Unexpected error: %s", str(e))
            raise HTTPException(status_code=500, detail="Internal server error")
    return wrapper

def convert_message_to_response(msg) -> Dict[str, Any]:
    """Convert ChatMessage to response format."""
    return {
        "id": str(msg.id),
        "content": msg.content,
        "role": msg.message_type,
        "timestamp": msg.created_at.isoformat(),
        "user_id": str(msg.user_id)
    }

@router.post("/ask", response_model=ChatResponse)
@handle_chat_exceptions
async def chat_ask(
    request: ChatRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    chat_service: ChatServiceInterface = Depends(get_chat_service)
) -> ChatResponse:
    """Process a chat request and return response."""
    history_service = get_history_service(db)
    session_id = str(current_user.id)
    
    # Save user message
    history_service.save_message(current_user.id, "user", request.message, session_id)
    
    # Get recent history and process request
    history = history_service.get_recent_history_as_dict(current_user.id, session_id)
    response = chat_service.process_chat_request(request, session_id, history)
    
    # Save assistant response
    history_service.save_message(current_user.id, "assistant", response, session_id)
    
    return ChatResponse(response=response)

@router.post("/send", response_model=ChatResponse)
async def chat_send(
    request: ChatRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    chat_service: ChatServiceInterface = Depends(get_chat_service)
) -> ChatResponse:
    """Alias for /ask endpoint to match frontend expectations."""
    return await chat_ask(request, current_user, db, chat_service)

@router.get("/history")
async def get_chat_history(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0)
) -> Dict[str, Any]:
    """Get chat history for the current user."""
    try:
        history_service = get_history_service(db)
        messages = history_service.get_history(current_user.id, limit, offset)
        total = history_service.get_message_count(current_user.id)
        
        return {
            "messages": [convert_message_to_response(msg) for msg in messages],
            "total": total
        }
    except Exception as e:
        logger.error("Error getting chat history: %s", str(e))
        raise HTTPException(status_code=500, detail="Error retrieving chat history")

@router.post("/clear")
async def clear_chat_history(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    """Clear chat history for the current user."""
    try:
        history_service = get_history_service(db)
        history_service.clear_history(current_user.id)
        return {"message": "Chat history cleared successfully"}
    except Exception as e:
        logger.error("Error clearing chat history: %s", str(e))
        raise HTTPException(status_code=500, detail="Error clearing chat history")

@router.get("/health")
async def chat_health(
    chat_service: ChatServiceInterface = Depends(get_chat_service)
) -> Dict[str, Any]:
    """Get chat service health status."""
    health_status = chat_service.health_check()
    
    return {
        "status": health_status.get("overall", "unknown"),
        "service": "chat",
        "version": "1.0.0",
        "checks": health_status,
        "features": [
            "RAG-powered responses",
            "Score filtering", 
            "Business type adaptation",
            "Conversation history"
        ]
    }

 