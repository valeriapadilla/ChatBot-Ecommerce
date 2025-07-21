from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON
from sqlalchemy.sql import func
from db.session import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    brand = Column(String(100), nullable=False)
    features = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    categories = Column(JSON, nullable=True, default=[])  # Store as JSON array
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"

    def to_dict(self):
        """Convert product to dictionary for API responses."""
        return {
            "id": self.id,
            "name": self.name,
            "brand": self.brand,
            "features": self.features,
            "price": self.price,
            "quantity": self.quantity,
            "categories": self.categories or [],
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }