import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models.product import Product
from app.interfaces.product_interface import ProductServiceInterface

logger = logging.getLogger(__name__)

class ProductService(ProductServiceInterface):
    """Service for product operations following single responsibility principle."""
    
    def __init__(self, db: Session):
        self.db = db

    def get_products(
        self,
        limit: int = 50,
        offset: int = 0,
        category: Optional[str] = None,
        brand: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[Product]:
        """Get products with optional filtering and pagination."""
        try:
            query = self.db.query(Product)
            
            # Apply filters
            if category:
                query = query.filter(text("categories::jsonb @> :category"))
                query = query.params(category=f'["{category}"]')
            
            if brand:
                query = query.filter(Product.brand.ilike(f"%{brand}%"))
            
            if min_price is not None:
                query = query.filter(Product.price >= min_price)
            
            if max_price is not None:
                query = query.filter(Product.price <= max_price)
            
            # Apply pagination
            products = query.offset(offset).limit(limit).all()
            
            logger.info(f"Retrieved {len(products)} products with filters: category={category}, brand={brand}, price_range={min_price}-{max_price}")
            return products
            
        except Exception as e:
            logger.error(f"Error fetching products: {str(e)}")
            raise

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get a specific product by ID."""
        try:
            product = self.db.query(Product).filter(Product.id == product_id).first()
            if product:
                logger.info(f"Retrieved product {product_id}: {product.name}")
            return product
            
        except Exception as e:
            logger.error(f"Error fetching product {product_id}: {str(e)}")
            raise

    def search_products(self, query: str, limit: int = 20) -> List[Product]:
        """Search products by name, brand, features, or categories."""
        try:
            sql_query = """
            SELECT * FROM products 
            WHERE name ILIKE :query 
            OR brand ILIKE :query 
            OR features ILIKE :query 
            OR categories::jsonb @> :category_json
            LIMIT :limit
            """
            
            products = self.db.query(Product).from_statement(
                text(sql_query)
            ).params(
                query=f"%{query}%",
                category_json=f'["{query}"]',
                limit=limit
            ).all()
            
            logger.info(f"Search for '{query}' returned {len(products)} results")
            return products
            
        except Exception as e:
            logger.error(f"Error searching products with query '{query}': {str(e)}")
            raise

    def get_categories(self) -> List[str]:
        """Get all available product categories."""
        try:
            products = self.db.query(Product).all()
            categories = set()
            
            for product in products:
                if product.categories:
                    categories.update(product.categories)
            
            categories_list = sorted(list(categories))
            logger.info(f"Retrieved {len(categories_list)} unique categories")
            return categories_list
            
        except Exception as e:
            logger.error(f"Error fetching categories: {str(e)}")
            raise

    def get_brands(self) -> List[str]:
        """Get all available product brands."""
        try:
            brands = self.db.query(Product.brand).distinct().all()
            brands_list = [brand[0] for brand in brands if brand[0]]
            
            logger.info(f"Retrieved {len(brands_list)} unique brands")
            return sorted(brands_list)
            
        except Exception as e:
            logger.error(f"Error fetching brands: {str(e)}")
            raise

    def get_all_products(self) -> List[Product]:
        """Get all products for recommendation system."""
        try:
            products = self.db.query(Product).all()
            logger.info(f"Retrieved {len(products)} total products")
            return products
            
        except Exception as e:
            logger.error(f"Error fetching all products: {str(e)}")
            raise 