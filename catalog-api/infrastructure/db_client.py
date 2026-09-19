import psycopg2
import psycopg2.extras
from core.config import settings


class DatabaseClient:
    """
    PostgreSQL + pgvector üzerinde kategori ve ürün arama operasyonlarını
    yöneten istemci. Hiçbir AI modeli içermez; ham sorgu sonuçlarını döner.
    """

    def __init__(self):
        self.conn = psycopg2.connect(**settings.DB_PARAMS)

    # ------------------------------------------------------------------
    # KATEGORİ SORGULARI
    # ------------------------------------------------------------------

    def get_top_candidates_by_vector(self, query_vector: list, limit: int = 20) -> list:
        """
        pgvector kosinüs mesafesi operatörü (<=>) ile en yakın kategori adaylarını döner.
        Sadece ham DB sonucu — re-ranking veya eşik filtresi yoktur.
        """
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = """
            SELECT id, name, full_path, description,
                   1 - (embedding <=> %s::vector) AS cosine_sim
            FROM categories
            WHERE embedding IS NOT NULL
              AND description IS NOT NULL
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
        """
        cur.execute(query, (str(query_vector), str(query_vector), limit))
        results = [dict(row) for row in cur.fetchall()]
        cur.close()
        return results

    def get_all_subcategory_ids(self, parent_ids: list) -> list:
        """Verilen kategori ID'lerinin kendilerini ve tüm alt kategori ID'lerini döner."""
        if not parent_ids:
            return []
        cur = self.conn.cursor()

        placeholders = ", ".join(["%s"] * len(parent_ids))
        cur.execute(
            f"SELECT full_path FROM categories WHERE id IN ({placeholders});",
            tuple(parent_ids),
        )
        paths = [row[0] for row in cur.fetchall() if row[0]]

        if not paths:
            cur.close()
            return parent_ids

        conditions = []
        params = []
        for path in paths:
            conditions.append("full_path = %s OR full_path LIKE %s")
            params.extend([path, path + "/%"])

        where_clause = " OR ".join(conditions)
        cur.execute(
            f"SELECT id FROM categories WHERE {where_clause};", tuple(params)
        )
        subcat_ids = list(set([row[0] for row in cur.fetchall()]))
        cur.close()
        return subcat_ids

    def get_main_categories(self, limit: int = 15) -> list:
        """Ana (level=1) kategorileri döner."""
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT DISTINCT id, name
            FROM categories
            WHERE name IS NOT NULL AND name != ''
            LIMIT %s;
            """,
            (limit,),
        )
        results = [{"id": row[0], "name": row[1]} for row in cur.fetchall()]
        cur.close()
        return results

    # ------------------------------------------------------------------
    # ÜRÜN SORGULARI
    # ------------------------------------------------------------------

    def get_products_by_vector_and_filters(
        self,
        query_vector: list,
        where_clause: str,
        filter_params: list,
        limit: int = 200,
    ) -> list:
        """
        pgvector kosinüs benzerliği + SQL filtrelerini birleştirerek ham ürün
        adaylarını döner. AI re-ranking bu serviste yapılmaz.
        """
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = f"""
            SELECT product_id, title, description, category_taxonomy,
                   image_url, brand, color, material, style, product_type,
                   model_year, clean_path, category_id,
                   1 - (embedding <=> %s::vector) AS cosine_sim
            FROM products
            WHERE {where_clause}
              AND embedding IS NOT NULL
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
        """
        full_params = [str(query_vector)] + filter_params + [str(query_vector), limit]
        cur.execute(query, tuple(full_params))
        results = [dict(row) for row in cur.fetchall()]
        cur.close()
        return results

    def get_products_by_category(self, category_id: str, limit: int = 50) -> list:
        """Belirli bir kategoriye ait ürünleri döner."""
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            """
            SELECT product_id, title, description, category_taxonomy,
                   image_url, brand, color, material, style, product_type,
                   model_year, clean_path, category_id
            FROM products
            WHERE category_id = %s
            LIMIT %s;
            """,
            (category_id, limit),
        )
        results = []
        for row in cur.fetchall():
            d = dict(row)
            d["cosine_sim"] = 1.0
            d["cross_encoder_score"] = 100.0
            results.append(d)
        cur.close()
        return results

    def get_product_by_id(self, product_id: str) -> dict | None:
        """Tek bir ürünü ID'ye göre döner."""
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute(
            """
            SELECT product_id, title, description, category_taxonomy,
                   image_url, brand, color, material, style, product_type,
                   model_year, clean_path, category_id
            FROM products
            WHERE product_id = %s
            LIMIT 1;
            """,
            (product_id,),
        )
        row = cur.fetchone()
        cur.close()
        return dict(row) if row else None
