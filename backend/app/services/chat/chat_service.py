import logging
from typing import List, Dict, Any
from app.schemas.chat import ChatRequest, ChatMessage
from app.services.rag.rag_service import ask_rag
from app.interfaces.chat_interface import ChatServiceInterface, HistoryConverterInterface, RequestValidatorInterface

logger = logging.getLogger(__name__)

class ChatService(ChatServiceInterface, HistoryConverterInterface, RequestValidatorInterface):    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def convert_history(self, history: List[ChatMessage]) -> List[dict]:
        """Convert ChatMessage objects to dictionary format."""
        if not history:
            return []
        return [{"role": msg.role, "content": msg.content} for msg in history]
    
    def validate_request(self, request: ChatRequest) -> None:
        """Validate chat request parameters."""
        if not request.message:
            raise ValueError("message is required")
        if request.k < 1 or request.k > 20:
            raise ValueError("k must be between 1 and 20")
        if request.max_score < 0 or request.max_score > 2.0:
            raise ValueError("max_score must be between 0.0 and 2.0")
    
    def process_chat_request(self, request: ChatRequest, user_id: str, history: List[Dict[str, str]] = None) -> str:
        """Process a chat request and return the response."""
        try:
            self.logger.info("Processing chat request for user %s", user_id)
            
            # Validate request
            self.validate_request(request)
            
            # Use provided history or empty list
            chat_history = history or []
            
            # Get response from RAG service
            response = ask_rag(
                user_id=user_id,
                message=request.message,
                history=chat_history,
                k=request.k,
                business_type=request.business_type,
                use_scores=request.use_scores,
                max_score=request.max_score
            )
            
            self.logger.info("Chat response generated successfully for user %s", user_id)
            return response
            
        except ValueError as e:
            self.logger.error("Validation error for user %s: %s", user_id, str(e))
            raise
        except Exception as e:
            self.logger.error("Error processing chat request for user %s: %s", user_id, str(e))
            raise
    
    def health_check(self) -> Dict[str, Any]:
        health_status = {
            "rag_service": "unknown",
            "vector_database": "unknown", 
            "llm_service": "unknown",
            "overall": "unknown"
        }
        
        try:
            test_request = ChatRequest(
                message="test",
                k=1,
                business_type="e-commerce",
                use_scores=False
            )
            
            response = self.process_chat_request(test_request, "health_check", [])
            
            if response and len(response) > 0:
                health_status.update({
                    "rag_service": "healthy",
                    "vector_database": "healthy",
                    "llm_service": "healthy", 
                    "overall": "healthy"
                })
            else:
                health_status.update({
                    "rag_service": "unhealthy",
                    "vector_database": "unhealthy",
                    "llm_service": "unhealthy",
                    "overall": "unhealthy"
                })
                
        except Exception as e:
            self.logger.error("Health check failed: %s", str(e))
            health_status.update({
                "rag_service": "failed",
                "vector_database": "failed", 
                "llm_service": "failed",
                "overall": "failed",
                "error": str(e)
            })
        
        return health_status 