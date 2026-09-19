"""
catalog-api — Uygulama giriş noktası.

Sorumluluk:
  - FastAPI uygulamasını başlat
  - Lifespan: DB bağlantısı ve ML modellerini yükle, DI'ya kaydet
  - Controller router'larını register et

İş mantığı veya AI kodu BURAYA yazılmaz.
"""

import sys
import os

# catalog-api dizinini Python path'e ekle
sys.path.insert(0, os.path.dirname(__file__))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.db_client import DatabaseClient
from infrastructure.ml_models import MLModels
import core.dependencies as deps

from controllers.categories_controller import router as categories_router
from controllers.products_controller import router as products_router


# ------------------------------------------------------------------
# Lifespan — uygulama başlangıç / bitiş
# ------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=" * 55)
    print("  ⏳ catalog-api başlatılıyor...")
    print("=" * 55)

    # 1. Veritabanı bağlantısı
    print("  📡 Veritabanı bağlantısı kuruluyor...")
    db = DatabaseClient()
    deps.set_db(db)
    print("  ✅ Veritabanı hazır.")

    # 2. ML modelleri yükle
    print("  🤖 ML modelleri yükleniyor (ilk seferde uzun sürebilir)...")
    ml = MLModels()
    deps.set_ml(ml)

    print("=" * 55)
    print("  ✅ catalog-api hazır!")
    print("=" * 55)

    yield

    print("  🔌 catalog-api kapanıyor...")


# ------------------------------------------------------------------
# Uygulama
# ------------------------------------------------------------------

app = FastAPI(
    title="AgenticCommerce — Catalog API",
    description=(
        "Ürün ve kategori arama servisi. "
        "Semantik arama (embedding + cross-encoder) + PostgreSQL/pgvector içerir."
    ),
    version="2.0.0",
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
# Router kayıtları
# ------------------------------------------------------------------

app.include_router(categories_router)
app.include_router(products_router)


# ------------------------------------------------------------------
# Genel endpoint'ler
# ------------------------------------------------------------------

@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "service": "catalog-api", "version": "2.0.0"}
