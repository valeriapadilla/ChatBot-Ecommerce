from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self):
        return self.db.query(Product).all()
    
    def get_by_id(self, product_id: int):
        return self.db.query(Product).filter(Product.id == product_id).first()