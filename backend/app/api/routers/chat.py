import logging
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
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

@router.post("/ask", response_model=ChatResponse)
async def chat_ask(
    request: ChatRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    chat_service: ChatServiceInterface = Depends(get_chat_service)
) -> ChatResponse:
    try:
        history_service = ChatHistoryService(db)
        history_service.save_message(current_user.id, "user", request.message, str(current_user.id))
        history = history_service.get_recent_history_as_dict(current_user.id, str(current_user.id))
        response = chat_service.process_chat_request(request, str(current_user.id), history)
        history_service.save_message(current_user.id, "assistant", response, str(current_user.id))
        return ChatResponse(response=response)
    except ChatValidationException as e:
        logger.warning("Validation error: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))
    except ChatProcessingException as e:
        logger.error("Processing error: %s", str(e))
        raise HTTPException(status_code=500, detail="Error processing chat request")
    except Exception as e:
        logger.error("Unexpected error: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/health")
async def chat_health(
    chat_service: ChatServiceInterface = Depends(get_chat_service)
) -> Dict[str, Any]:
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

 