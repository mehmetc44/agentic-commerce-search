"""
dependencies.py — FastAPI Dependency Injection merkezi.

Uygulama genelinde paylaşılan singleton'lar (db, ml_models, servisler)
bu modül üzerinden Depends() ile inject edilir.

Kullanım:
    @router.post("/categories/search")
    async def search(
        request: CategorySearchRequest,
        svc: CategoryService = Depends(get_category_service),
    ): ...
"""

from functools import lru_cache
from infrastructure.db_client import DatabaseClient
from infrastructure.ml_models import MLModels
from services.category_service import CategoryService
from services.product_service import ProductService

# ------------------------------------------------------------------
# Uygulama başlatıldığında (lifespan) set edilir
# ------------------------------------------------------------------
_db: DatabaseClient | None = None
_ml: MLModels | None = None


def set_db(db: DatabaseClient) -> None:
    global _db
    _db = db


def set_ml(ml: MLModels) -> None:
    global _ml
    _ml = ml


# ------------------------------------------------------------------
# FastAPI Depends() fonksiyonları
# ------------------------------------------------------------------


def get_db() -> DatabaseClient:
    """Paylaşılan veritabanı istemcisini döner."""
    return _db


def get_ml() -> MLModels:
    """Paylaşılan ML modelleri döner (embedding + cross-encoder)."""
    return _ml


def get_category_service() -> CategoryService:
    """Her istek için CategoryService instance'ı döner (servis stateless)."""
    return CategoryService(db=_db, ml=_ml)


def get_product_service() -> ProductService:
    """Her istek için ProductService instance'ı döner (servis stateless)."""
    return ProductService(db=_db, ml=_ml)
