from fastapi import APIRouter, HTTPException
from app.api.dependencies import get_container

router = APIRouter()

@router.get("/categories", tags=["Catalog"])
async def get_categories():
    """Ana menü ve sidebar için ana kategorileri getirir."""
    container = get_container()
    try:
        categories = container.db_client.get_main_categories(limit=15)
        return {"data": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products/category/{category_id}", tags=["Catalog"])
async def get_category_products(category_id: str):
    """Bir kategoriye ait ürünleri getirir."""
    container = get_container()
    try:
        products = container.db_client.get_products_by_category(category_id, limit=50)
        return {"data": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products/{product_id}", tags=["Catalog"])
async def get_single_product(product_id: str):
    """Ürün detay sayfası için tek bir ürünün bilgilerini getirir."""
    container = get_container()
    try:
        product = container.db_client.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Ürün bulunamadı")
        return {"data": product}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
