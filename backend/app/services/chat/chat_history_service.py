from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict, Any
from app.models.chat_message import ChatMessage
from app.interfaces.chat_history_interface import ChatHistoryServiceInterface

class ChatHistoryService(ChatHistoryServiceInterface):
    def __init__(self, db: Session):
        self.db = db

    def save_message(self, user_id: int, message_type: str, content: str, session_id: str):
        """Save a new chat message."""
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

    def get_recent_history(self, user_id: int, session_id: str, limit: int = 10) -> List[ChatMessage]:
        """Get recent chat history for a specific session."""
        return self._get_messages_by_session(user_id, session_id, limit)

    def get_recent_history_as_dict(self, user_id: int, session_id: str, limit: int = 10) -> List[Dict[str, str]]:
        """Get recent chat history as a list of dictionaries for LangChain."""
        messages = self.get_recent_history(user_id, session_id, limit)
        return self._convert_messages_to_dict(messages)

    def get_history(self, user_id: int, limit: int = 50, offset: int = 0) -> List[ChatMessage]:
        """Get paginated chat history for a user."""
        return self._get_messages_by_user(user_id, limit, offset)

    def get_message_count(self, user_id: int) -> int:
        """Get total number of messages for a user."""
        return self._count_messages_by_user(user_id)

    def clear_history(self, user_id: int) -> None:
        """Clear all chat history for a user."""
        self._delete_messages_by_user(user_id)

    def _get_messages_by_session(self, user_id: int, session_id: str, limit: int) -> List[ChatMessage]:
        """Private method to get messages by session with common query logic."""
        messages = (
            self.db.query(ChatMessage)
            .filter(
                ChatMessage.user_id == user_id,
                ChatMessage.session_id == session_id
            )
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
            .all()
        )
        return messages[::-1]  # Reverse to get chronological order

    def _get_messages_by_user(self, user_id: int, limit: int, offset: int) -> List[ChatMessage]:
        """Private method to get messages by user with pagination."""
        messages = (
            self.db.query(ChatMessage)
            .filter(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return messages[::-1]  # Reverse to get chronological order

    def _count_messages_by_user(self, user_id: int) -> int:
        """Private method to count messages by user."""
        count = (
            self.db.query(func.count(ChatMessage.id))
            .filter(ChatMessage.user_id == user_id)
            .scalar()
        )
        return count or 0

    def _delete_messages_by_user(self, user_id: int) -> None:
        """Private method to delete messages by user."""
        (
            self.db.query(ChatMessage)
            .filter(ChatMessage.user_id == user_id)
            .delete()
        )
        self.db.commit()

    def _convert_messages_to_dict(self, messages: List[ChatMessage]) -> List[Dict[str, str]]:
        """Private method to convert messages to dictionary format."""
        return [
            {
                "role": msg.message_type,
                "content": msg.content
            }
            for msg in messages
        ] 