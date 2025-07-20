from sqlalchemy.orm import Session
from app.models.chat_message import ChatMessage
from app.interfaces.chat_history_interface import ChatHistoryServiceInterface

class ChatHistoryService(ChatHistoryServiceInterface):
    def __init__(self, db: Session):
        self.db = db

    def save_message(self, user_id: int, message_type: str, content: str, session_id: str):
        message = ChatMessage(
            user_id=user_id,
            message_type=message_type,
            content=content,
            session_id=session_id
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_recent_history(self, user_id: int, session_id: str, limit: int = 10):
        messages = (
            self.db.query(ChatMessage)
            .filter(ChatMessage.user_id == user_id, ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
            .all()
        )[::-1]
        return messages
    
    def get_recent_history_as_dict(self, user_id: int, session_id: str, limit: int = 10):
        """Get recent chat history as a list of dictionaries for LangChain."""
        messages = self.get_recent_history(user_id, session_id, limit)
        return [
            {
                "role": msg.message_type,  # "user" or "assistant"
                "content": msg.content
            }
            for msg in messages
        ] 