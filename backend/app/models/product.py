from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    
    id       = Column(Integer, primary_key=True, index=True)
    name     = Column(String,  nullable=False)
    brand    = Column(String,  nullable=False)
    features = Column(Text,    nullable=True)
    price    = Column(Float,   nullable=False)
    quantity = Column(Integer, nullable=False)