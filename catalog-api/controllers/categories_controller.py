"""
categories_controller.py — /categories/* route handler'ları.

Sorumluluk: Sadece HTTP katmanı.
  - Request'i al → Service'e ilet → Sonucu döndür.
  - Hiçbir iş mantığı veya AI kodu içermez.
"""

from fastapi import APIRouter, Depends, HTTPException
from models.category_models import (
    CategorySearchRequest,
    CategorySearchResponse,
    CategoryResult,
)
from services.category_service import CategoryService
from core.dependencies import get_category_service, get_db

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", summary="Ana kategorileri listele")
async def list_categories(
    limit: int = 15,
    db=Depends(get_db),
):
    """Ana kategori listesini döner."""
    try:
        categories = db.get_main_categories(limit=limit)
        return {"data": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/search",
    response_model=CategorySearchResponse,
    summary="Semantik kategori araması",
)
async def search_categories(
    request: CategorySearchRequest,
    svc: CategoryService = Depends(get_category_service),
):
    """
    Doğal dil query'i alır.
    Embedding + pgvector + CrossEncoder pipeline ile en alakalı kategorileri döner.
    """
    try:
        results = svc.search(query=request.query, limit=request.limit)
        return CategorySearchResponse(
            data=[CategoryResult(**r) for r in results]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{category_id}/filters", summary="Kategori filtrelerini getir")
async def get_category_filters(category_id: str):
    """
    Belirli bir kategorideki ürünler için kullanılabilir filtreleri döner.
    İleride DB'den çekilebilir; şimdilik genel filtre şeması.
    """
    filters = ["brand", "color", "min_price", "max_price"]
    return {
        "data": {
            "available_filters": filters,
            "instruction": "Müşteriye bu filtrelerle ilgili tercihi olup olmadığını sorabilirsiniz.",
        }
    }
