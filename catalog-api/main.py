"""
catalog-api — FastAPI uygulaması

Sorumluluk: Sadece ham veritabanı işlemleri.
- Kategori vektör araması (pgvector)
- Ürün vektör araması + SQL filtreleme (pgvector)
- Kategori listeleme
- Ürün listeleme / tek ürün getirme

AI modeli (embedding, cross-encoder) içermez.
Vektörler çağrıcı (AI servisi) tarafından hesaplanıp gönderilir.
"""

import sys
import os

# catalog-api/ dizinini Python path'e ekle
sys.path.insert(0, os.path.dirname(__file__))

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from infrastructure.db_client import DatabaseClient
from services.sql_filter_parser import SQLFilterParser

# ------------------------------------------------------------------
# Uygulama başlangıcında DB istemcisini başlat
# ------------------------------------------------------------------
db: DatabaseClient | None = None
sql_parser = SQLFilterParser()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global db
    print("⏳ [Catalog API] Veritabanı bağlantısı kuruluyor...")
    db = DatabaseClient()
    print("✅ [Catalog API] Hazır.")
    yield
    print("🔌 [Catalog API] Kapanıyor...")


app = FastAPI(
    title="AgenticCommerce — Catalog API",
    description="Ürün ve kategori veritabanı işlemleri. AI modeli içermez.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------
# REQUEST / RESPONSE MODELLER
# ------------------------------------------------------------------


class CategoryVectorSearchRequest(BaseModel):
    query_vector: list[float]
    limit: int = 20


class ProductVectorSearchRequest(BaseModel):
    query_vector: list[float]
    category_ids: list[str] = []
    brand: Optional[str] = None
    color: Optional[str] = None
    limit: int = 200


# ------------------------------------------------------------------
# KATEGORİ ENDPOINTLERİ
# ------------------------------------------------------------------


@app.get("/health")
async def health():
    return {"status": "ok", "service": "catalog-api"}


@app.get("/categories")
async def get_main_categories(limit: int = 15):
    """Ana kategorileri döner."""
    try:
        categories = db.get_main_categories(limit=limit)
        return {"data": categories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/categories/vector-search")
async def category_vector_search(request: CategoryVectorSearchRequest):
    """
    Verilen query_vector ile pgvector kosinüs araması yapar.
    Ham aday kategorileri (id, name, full_path, description, cosine_sim) döner.
    Re-ranking veya eşik filtresi yapılmaz — bu AI servisinin görevidir.
    """
    try:
        candidates = db.get_top_candidates_by_vector(
            query_vector=request.query_vector, limit=request.limit
        )
        return {"data": candidates}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/categories/{category_id}/filters")
async def get_category_filters(category_id: str):
    """
    Kategoriye özel kullanılabilir filtreleri döner.
    Şimdilik genel filtre listesi; ileride DB'den çekilebilir.
    """
    filters = ["brand", "color", "min_price", "max_price"]
    return {
        "data": {
            "available_filters": filters,
            "instruction": "Müşteriye bu filtrelerle ilgili tercihi olup olmadığını sorabilirsiniz.",
        }
    }


# ------------------------------------------------------------------
# ÜRÜN ENDPOINTLERİ
# ------------------------------------------------------------------


@app.post("/products/vector-search")
async def product_vector_search(request: ProductVectorSearchRequest):
    """
    Verilen query_vector + filtreler ile pgvector + SQL araması yapar.
    Ham aday ürünleri döner. Cross-encoder re-ranking AI servisinde yapılır.
    """
    try:
        # Kategori ID'lerini alt kategorilere genişlet
        expanded_ids = []
        if request.category_ids:
            expanded_ids = db.get_all_subcategory_ids(request.category_ids)
            print(
                f"    🌲 Kategori genişletme: {len(request.category_ids)} → {len(expanded_ids)} alt kategori"
            )

        # Filtreleri oluştur
        extracted_filters: dict = {}
        if expanded_ids:
            extracted_filters["category_taxonomy"] = expanded_ids
        if request.brand:
            extracted_filters["brand"] = request.brand
        if request.color:
            extracted_filters["color"] = [request.color]

        where_clause, filter_params = sql_parser.parse_filters(extracted_filters)
        print(f"    🔍 SQL WHERE: {where_clause}")

        candidates = db.get_products_by_vector_and_filters(
            query_vector=request.query_vector,
            where_clause=where_clause,
            filter_params=filter_params,
            limit=request.limit,
        )
        print(f"    📦 {len(candidates)} ham aday ürün döndürülüyor.")
        return {"data": candidates}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/products/category/{category_id}")
async def get_products_by_category(category_id: str, limit: int = 50):
    """Belirli bir kategoriye ait ürünleri döner."""
    try:
        products = db.get_products_by_category(category_id=category_id, limit=limit)
        return {"data": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/products/{product_id}")
async def get_product_by_id(product_id: str):
    """Tek bir ürünü ID'ye göre döner."""
    try:
        product = db.get_product_by_id(product_id=product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Ürün bulunamadı.")
        return {"data": product}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
