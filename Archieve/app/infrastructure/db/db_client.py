import psycopg2
from app.core.config import settings

class DatabaseClient:
    """PostgreSQL + pgvector üzerinde kategori arama operasyonlarını yöneten istemci."""
    def __init__(self):
        self.conn = psycopg2.connect(**settings.DB_PARAMS)
        
    def get_top_candidates_by_vector(self, query_vector: list, limit: int = 20) -> list:
        """1. AŞAMA: pgvector ile tüm veritabanını tarar ve en yakın Top 20 adayı getirir."""
        cur = self.conn.cursor()
        
        # pgvector'ün <=> (Kosinüs Mesafesi) operatörü ile ışık hızında vektör araması
        query = """
            SELECT id, name, full_path, description, 
                   1 - (embedding <=> %s::vector) AS cosine_sim
            FROM categories
            WHERE embedding IS NOT NULL
              AND description IS NOT NULL
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
        """
        # Vector parametrelerini stringe çevirerek SQL'e paslıyoruz
        cur.execute(query, (str(query_vector), str(query_vector), limit))
        
        results = [
            {
                "id": row[0], 
                "name": row[1], 
                "full_path": row[2], 
                "description": row[3],
                "score": row[4]
            } 
            for row in cur.fetchall()
        ]
        cur.close()
        return results

    def get_all_subcategory_ids(self, parent_ids: list) -> list:
        """Verilen kategori ID'lerinin kendilerini ve tüm alt kategori ID'lerini döner."""
        if not parent_ids:
            return []
        cur = self.conn.cursor()
        
        # 1. Parent kategorilerin full_path'lerini çek
        placeholders = ', '.join(['%s'] * len(parent_ids))
        query_paths = f"SELECT full_path FROM categories WHERE id IN ({placeholders});"
        cur.execute(query_paths, tuple(parent_ids))
        paths = [row[0] for row in cur.fetchall() if row[0]]
        
        if not paths:
            cur.close()
            return parent_ids # Fallback: eğer path bulunamazsa kendilerini dön
            
        # 2. Bu path'lerin kendisi veya alt yolu olan tüm kategorileri bul
        conditions = []
        params = []
        for path in paths:
            conditions.append("full_path = %s OR full_path LIKE %s")
            params.extend([path, path + "/%"])
            
        where_clause = " OR ".join(conditions)
        query_subcats = f"SELECT id FROM categories WHERE {where_clause};"
        cur.execute(query_subcats, tuple(params))
        
        subcat_ids = list(set([row[0] for row in cur.fetchall()]))
        cur.close()
        return subcat_ids

    def get_products_by_vector_and_filters(self, query_vector: list, where_clause: str, filter_params: list, limit: int = 100) -> list:
        """2. AŞAMA: Vektör benzerliği ve SQL filtrelerini birleştirerek ürünleri getirir."""
        cur = self.conn.cursor()
        
        query = f"""
            SELECT product_id, title, description, category_taxonomy, image_url, brand, color, material, style, product_type, model_year, clean_path, category_id,
                   1 - (embedding <=> %s::vector) AS cosine_sim
            FROM products
            WHERE {where_clause}
              AND embedding IS NOT NULL
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
        """
        
        full_params = [str(query_vector)] + filter_params + [str(query_vector), limit]
        cur.execute(query, tuple(full_params))
        
        results = []
        for row in cur.fetchall():
            results.append({
                "product_id": row[0],
                "title": row[1],
                "description": row[2],
                "category_taxonomy": row[3],
                "image_url": row[4],
                "brand": row[5],
                "color": row[6],
                "material": row[7],
                "style": row[8],
                "product_type": row[9],
                "model_year": row[10],
                "clean_path": row[11],
                "category_id": row[12],
                "cosine_sim": row[13],
                "cross_encoder_score": 100.0 # UI compatibility for non-ai searches
            })
        cur.close()
        return results
        
    def get_main_categories(self, limit: int = 15) -> list:
        cur = self.conn.cursor()
        # Fetching a random distinct set of categories since we don't have parent_id
        # Alternatively we order by some metric, here just getting limit
        query = """
            SELECT DISTINCT id, name 
            FROM categories 
            WHERE name IS NOT NULL AND name != ''
            LIMIT %s;
        """
        cur.execute(query, (limit,))
        results = [{"id": row[0], "name": row[1]} for row in cur.fetchall()]
        cur.close()
        return results

    def get_products_by_category(self, category_id: str, limit: int = 50) -> list:
        cur = self.conn.cursor()
        query = """
            SELECT product_id, title, description, category_taxonomy, image_url, brand, color, material, style, product_type, model_year, clean_path, category_id
            FROM products
            WHERE category_id = %s
            LIMIT %s;
        """
        cur.execute(query, (category_id, limit))
        results = []
        for row in cur.fetchall():
            results.append({
                "product_id": row[0],
                "title": row[1],
                "description": row[2],
                "category_taxonomy": row[3],
                "image_url": row[4],
                "brand": row[5],
                "color": row[6],
                "material": row[7],
                "style": row[8],
                "product_type": row[9],
                "model_year": row[10],
                "clean_path": row[11],
                "category_id": row[12],
                "cosine_sim": 1.0,
                "cross_encoder_score": 100.0 # Default max for UI
            })
        cur.close()
        return results

    def get_product_by_id(self, product_id: str) -> dict:
        cur = self.conn.cursor()
        query = """
            SELECT product_id, title, description, category_taxonomy, image_url, brand, color, material, style, product_type, model_year, clean_path, category_id
            FROM products
            WHERE product_id = %s
            LIMIT 1;
        """
        cur.execute(query, (product_id,))
        row = cur.fetchone()
        cur.close()
        
        if not row:
            return None
            
        return {
            "product_id": row[0],
            "title": row[1],
            "description": row[2],
            "category_taxonomy": row[3],
            "image_url": row[4],
            "brand": row[5],
            "color": row[6],
            "material": row[7],
            "style": row[8],
            "product_type": row[9],
            "model_year": row[10],
            "clean_path": row[11],
            "category_id": row[12]
        }
