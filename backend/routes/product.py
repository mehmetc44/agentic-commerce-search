from fastapi import APIRouter, Query, HTTPException
from backend.repositories.ProductRepository import ProductRepository
from backend.services.ProductService import ProductService

router = APIRouter()

# Dependency (ASP.NET -> DI gibi düşün)
# Eski CSV'ler yerine yeni ChromaDB Persistent Client yolunu veriyoruz.
repo = ProductRepository(db_path="./data", collection_name="ecommerce_products")
service = ProductService(repo)


# 🔹 1. Pagination (ANA ENDPOINT)
@router.get("/products")
def get_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(40, ge=1, le=100)
):
    products = service.get_paginated(page, page_size)

    return {
        "page": page,
        "page_size": page_size,
        "count": len(products),
        "data": [p.model_dump() for p in products] # Pydantic nesnesini JSON'a çeviriyoruz
    }


# 🔹 2. ID (parent_asin) ile ürün getir
@router.get("/product/{product_id}")
def get_product(product_id: str):
    product = repo.get_by_id(product_id)

    if product:
        return product.model_dump()

    # FastAPI'de standart hata fırlatma yöntemi (ASP.NET'teki NotFound() gibi)
    raise HTTPException(status_code=404, detail="Ürün bulunamadı")


# 🔹 3. Kategoriye göre ürünler
# DİKKAT: Artık category_id (int) değil, category_name (str) kullanıyoruz
@router.get("/products/category/{category_name}")
def get_products_by_category(category_name: str, limit: int = Query(40, le=100)):
    products = service.get_by_category(category_name=category_name, limit=limit)

    return {
        "category": category_name,
        "count": len(products),
        "data": [p.model_dump() for p in products]
    }


# 🔹 4. Fiyata göre filtre
@router.get("/products/price")
def get_products_by_price(max_price: float, limit: int = Query(40, le=100)):
    products = service.get_by_price_less_than(price=max_price, limit=limit)

    return {
        "max_price": max_price,
        "count": len(products),
        "data": [p.model_dump() for p in products]
    }


# 🔹 5. Kategori + fiyat
@router.get("/products/filter")
def get_products_by_category_and_price(
    category_name: str = Query(..., description="Kategori adı"),
    max_price: float = Query(..., description="Maksimum fiyat"),
    limit: int = Query(40, le=100)
):
    products = service.get_by_category_and_price(category_name=category_name, price=max_price, limit=limit)

    return {
        "category": category_name,
        "max_price": max_price,
        "count": len(products),
        "data": [p.dict() for p in products]
    }