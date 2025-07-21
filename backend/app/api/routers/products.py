import logging
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.product import ProductResponse
from app.api.deps import get_db, get_current_active_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductResponse])
async def get_products(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    category: Optional[str] = Query(None),
    brand: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all products with optional filtering and pagination."""
    try:
        from app.services.product.product_service import ProductService
        product_service = ProductService(db)
        
        products = product_service.get_products(
            limit=limit,
            offset=offset,
            category=category,
            brand=brand,
            min_price=min_price,
            max_price=max_price
        )
        return [product.to_dict() for product in products]
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching products")

@router.get("/search", response_model=List[ProductResponse])
async def search_products(
    query: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Search products by name, brand, features, or categories."""
    try:
        from app.services.product.product_service import ProductService
        product_service = ProductService(db)
        
        products = product_service.search_products(query=query, limit=limit)
        return [product.to_dict() for product in products]
    except Exception as e:
        logger.error(f"Error searching products: {str(e)}")
        raise HTTPException(status_code=500, detail="Error searching products")

@router.get("/categories/list")
async def get_categories(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all available product categories."""
    try:
        from app.services.product.product_service import ProductService
        product_service = ProductService(db)
        
        categories = product_service.get_categories()
        return {
            "categories": categories,
            "count": len(categories),
            "user_id": current_user.id
        }
    except Exception as e:
        logger.error(f"Error fetching categories: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching categories")

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific product by ID."""
    try:
        from app.services.product.product_service import ProductService
        product_service = ProductService(db)
        
        product = product_service.get_product_by_id(product_id)
        
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return product.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching product: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching product")

@router.get("/brands/list")
async def get_brands(
    db: Session = Depends(get_db)
):
    try:
        from app.services.product.product_service import ProductService
        product_service = ProductService(db)
        
        brands = product_service.get_brands()
        return {
            "brands": brands,
            "count": len(brands)
        }
    except Exception as e:
        logger.error(f"Error fetching brands: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching brands")
