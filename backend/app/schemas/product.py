from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class ProductResponse(BaseModel):
    id: int
    name: str
    brand: str
    features: str | None
    price: float
    quantity: int
    categories: List[str] = []
    image_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
