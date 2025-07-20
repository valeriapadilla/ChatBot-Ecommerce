from pydantic import BaseModel

class ProductOut(BaseModel):
    id: int
    name: str
    brand: str
    features: str | None
    price: float
    quantity: int

    class Config:
        orm_mode = True
