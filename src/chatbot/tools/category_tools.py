from langchain_core.tools import tool
import json
from chatbot.services.container import container

@tool
def get_closest_categories(sample_query: str) -> str:
    """
    Kullanıcının aradığı ürünün veya isteğin olabileceği en mantıklı kategorileri veritabanından semantik (vektör) aramayla bulur.
    
    Args:
        sample_query: Kullanıcının niyetini anlatan cümle (Örn: 'kamp için su geçirmez çadır' veya 'kırmızı elbise').
        
    Returns:
        JSON string formatında, eşleşen kategorilerin ID'lerini ve isimlerini döner.
    """
    try:
        # Category matcher uses get_matched_category_ids which returns just IDs. 
        # But wait, we want to return IDs AND names so the LLM understands what they are.
        # Let's bypass the strict threshold if we just want top K categories to give the LLM options.
        clean_query = container.category_matcher._clean_query_for_semantic_models(sample_query)
        query_vector = container.embedding_model.encode(clean_query, convert_to_tensor=False).tolist()
        candidates = container.db_client.get_top_candidates_by_vector(query_vector, limit=10)
        
        # Only return the top 5 logical categories to the LLM
        results = []
        for c in candidates[:5]:
            results.append({
                "id": c["id"],
                "name": c["name"],
                "full_path": c["full_path"]
            })
            
        return json.dumps(results, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)})

@tool
def get_category_filters(category_id: str) -> str:
    """
    Belirli bir kategorideki ürünleri daraltmak için hangi filtrelerin (örn: beden, renk, hafıza) kullanılabileceğini döner.
    LLM bu filtreleri kullanarak müşteriye spesifik sorular sorabilir.
    
    Args:
        category_id: Filtreleri öğrenilecek kategorinin ID'si.
        
    Returns:
        JSON string formatında kullanılabilir filtre listesi.
    """
    # In a real scenario, this would query a taxonomy table. 
    # For now, we will mock common dynamic filters based on typical e-commerce, 
    # or extract distinct columns from the products table for this category.
    # We will just return a generalized schema to guide the LLM.
    
    # Generic logic for demonstration:
    filters = ["brand", "color", "min_price", "max_price"]
    
    # In future, you can add DB calls like: `SELECT DISTINCT material FROM products WHERE category_id=...`
    
    return json.dumps({
        "available_filters": filters,
        "instruction": "Müşteriye bu filtrelerle ilgili tercihi olup olmadığını sorabilirsiniz."
    }, ensure_ascii=False)
