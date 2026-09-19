"""
products_controller.py — /products/* route handler'ları.

Sorumluluk: Sadece HTTP katmanı.
  - Request'i al → Service'e ilet → Sonucu döndür.
  - Hiçbir iş mantığı veya AI kodu içermez.
"""

from fastapi import APIRouter, Depends, HTTPException
from models.product_models import (
    ProductSearchRequest,
    ProductSearchResponse,
    ProductResult,
)
from services.product_service import ProductService
from core.dependencies import get_product_service, get_db

router = APIRouter(prefix="/products", tags=["Products"])


@router.post(
    "/search",
    response_model=ProductSearchResponse,
    summary="Semantik ürün araması",
)
async def search_products(
    request: ProductSearchRequest,
    svc: ProductService = Depends(get_product_service),
):
    """
    Doğal dil query'i ve filtreleri alır.
    Embedding + pgvector + SQL filter + CrossEncoder pipeline ile
    en alakalı ürünleri döner.
    """
    try:
        results = svc.search(
            query=request.query,
            category_ids=request.category_ids,
            brand=request.brand,
            color=request.color,
            max_results=request.max_results,
        )
        return ProductSearchResponse(
            data=[ProductResult(**r) for r in results]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/category/{category_id}", summary="Kategoriye göre ürün listele")
async def list_products_by_category(
    category_id: str,
    limit: int = 50,
    db=Depends(get_db),
):
    """Belirli bir kategoriye ait ürünleri döner."""
    try:
        products = db.get_products_by_category(
            category_id=category_id, limit=limit
        )
        return {"data": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{product_id}", summary="Tekil ürün detayı")
async def get_product(product_id: str, db=Depends(get_db)):
    """Ürün ID'ye göre tek ürün getirir."""
    try:
        product = db.get_product_by_id(product_id=product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Ürün bulunamadı.")
        return {"data": product}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
