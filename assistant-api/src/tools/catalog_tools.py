from langchain_core.tools import tool

@tool
def get_closest_categories(query: str) -> list[dict]:
    """Kullanıcının aramasına en uygun kategorileri veritabanından bulur."""
    # TODO: MCP veya catalog-api üzerinden doldurulacak
    raise NotImplementedError("Henüz implement edilmedi")

@tool
def list_closest_products(category_id: int, query: str, limit: int = 5) -> list[dict]:
    """Belirli bir kategorideki en uygun ürünleri listeler."""
    # TODO: MCP veya catalog-api üzerinden doldurulacak
    raise NotImplementedError("Henüz implement edilmedi")

@tool
def get_category_filters(category_id: int) -> dict:
    """Kategoriye ait dinamik filtreleri (renk, beden, marka vb.) getirir."""
    # TODO: MCP veya catalog-api üzerinden doldurulacak
    raise NotImplementedError("Henüz implement edilmedi")
