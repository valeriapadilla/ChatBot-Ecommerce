import logging
import time
from typing import List, Dict, Any
from app.rag.retriever import get_retriever
from app.llm.client import generate_chat_completion
from app.services.chat.prompt_builder import build_chat_prompt
from app.interfaces.rag_interface import RAGServiceInterface

logger = logging.getLogger(__name__)


class RAGService(RAGServiceInterface):
    def __init__(self, k: int = 3, business_type: str = "e-commerce", use_scores: bool = False, max_score: float = 1.2):
        self.k = k
        self.business_type = business_type
        self.use_scores = use_scores
        self.max_score = max_score
        self.retriever = get_retriever(k=self.k, use_scores=use_scores, max_score=max_score)

    def ask(
        self,
        user_id: str,
        message: str,
        history: List[Dict[str, str]] = None
    ) -> str:
        try:
            start_time = time.time()            
            docs = self.retriever.invoke(message)

            prompt_messages = build_chat_prompt(
                docs=docs,
                user_msg=message,
                history=history or [],
                business_type=self.business_type
            )

            reply = generate_chat_completion(prompt_messages)
            
            processing_time = time.time() - start_time
            logger.info("Chat response generated in %.3fs for user %s", processing_time, user_id)
            
            return reply
            
        except Exception as e:
            logger.error("Error in ask method: %s", str(e))
            raise


def ask_rag(
    user_id: str,
    message: str,
    history: List[Dict[str, str]] = None,
    k: int = 3,
    business_type: str = "e-commerce",
    use_scores: bool = False,
    max_score: float = 1.2
) -> str: 
    service = RAGService(k=k, business_type=business_type, use_scores=use_scores, max_score=max_score)
    return service.ask(user_id, message, history) 