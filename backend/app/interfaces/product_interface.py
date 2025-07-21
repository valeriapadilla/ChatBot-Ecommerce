from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.product import Product

class ProductServiceInterface(ABC):
    """Interface for product service following SOLID principles."""
    
    @abstractmethod
    def get_products(
        self,
        limit: int = 50,
        offset: int = 0,
        category: Optional[str] = None,
        brand: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[Product]:
        """
        Get products with optional filtering and pagination.
        
        Args:
            limit: Number of products to return
            offset: Number of products to skip
            category: Filter by category
            brand: Filter by brand
            min_price: Minimum price filter
            max_price: Maximum price filter
            
        Returns:
            List of products matching criteria
        """
        pass
    
    @abstractmethod
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """
        Get a specific product by ID.
        
        Args:
            product_id: The unique identifier of the product
            
        Returns:
            Product object or None if not found
        """
        pass
    
    @abstractmethod
    def search_products(self, query: str, limit: int = 20) -> List[Product]:
        """
        Search products by name, brand, features, or categories.
        
        Args:
            query: Search term
            limit: Maximum number of results
            
        Returns:
            List of products matching search criteria
        """
        pass
    
    @abstractmethod
    def get_categories(self) -> List[str]:
        """
        Get all available product categories.
        
        Returns:
            List of unique category names
        """
        pass
    
    @abstractmethod
    def get_brands(self) -> List[str]:
        """
        Get all available product brands.
        
        Returns:
            List of unique brand names
        """
        pass
    
    @abstractmethod
    def get_all_products(self) -> List[Product]:
        """
        Get all products for recommendation system.
        
        Returns:
            List of all products
        """
        pass 