from fastapi import APIRouter, Query
from backend.repositories.ProductRepository import ProductRepository
from backend.services.ProductService import ProductService

router = APIRouter()

# Dependency (ASP.NET -> DI gibi düşün)
repo = ProductRepository("data/amazon_categories.csv", "data/amazon_products.csv")
service = ProductService(repo)


# 🔹 1. Pagination (ANA ENDPOINT)
@router.get("/products")
def get_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(40, ge=1, le=100)
):
    products = list(service.get_paginated(page, page_size))

    return {
        "page": page,
        "page_size": page_size,
        "count": len(products),
        "data": products
    }


# 🔹 2. ID ile ürün getir
@router.get("/product/{product_id}")
def get_product(product_id: str):
    product = repo.get_by_id(product_id)

    if product:
        return product

    return {"error": "Ürün bulunamadı"}


# 🔹 3. Kategoriye göre ürünler
@router.get("/products/category/{category_id}")
def get_products_by_category(category_id: int):
    products = list(service.get_by_category(category_id))

    return {
        "category_id": category_id,
        "count": len(products),
        "data": products
    }


# 🔹 4. Fiyata göre filtre
@router.get("/products/price")
def get_products_by_price(max_price: float):
    products = list(service.get_by_price_less_than(max_price))

    return {
        "max_price": max_price,
        "count": len(products),
        "data": products
    }


# 🔹 5. Kategori + fiyat
@router.get("/products/filter")
def get_products_by_category_and_price(
    category_id: int,
    max_price: float
):
    products = list(service.get_by_category_and_price(category_id, max_price))

    return {
        "category_id": category_id,
        "max_price": max_price,
        "count": len(products),
        "data": products
    }