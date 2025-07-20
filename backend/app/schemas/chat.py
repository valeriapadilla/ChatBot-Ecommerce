from typing import List, Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Schema for a single chat message."""
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")


class ChatRequest(BaseModel):
    """Schema for chat request."""
    message: str = Field(..., description="User's message")
    k: Optional[int] = Field(default=8, ge=1, le=20, description="Number of documents to retrieve")
    business_type: Optional[str] = Field(default="e-commerce", description="Type of business context")
    use_scores: Optional[bool] = Field(default=False, description="Whether to filter by similarity scores")
    max_score: Optional[float] = Field(default=1.2, ge=0.0, le=2.0, description="Maximum score threshold")


class ChatResponse(BaseModel):
    """Schema for chat response."""
    response: str = Field(..., description="Assistant's response")



 