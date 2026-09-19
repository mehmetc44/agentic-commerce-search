from fastapi import APIRouter, HTTPException
from typing import List
from services.product_service import ProductService
from models.schemas import ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])
service = ProductService()

@router.get("/", response_model=List[ProductResponse])
def get_products(limit: int = 100):
    try:
        return service.get_products(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    try:
        product = service.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
