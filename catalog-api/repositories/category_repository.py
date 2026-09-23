from context.DBContext import DBContext
from psycopg2.extras import RealDictCursor

class CategoryRepository:
    def get_all(self, limit: int = 100):
        conn = DBContext.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM categories LIMIT %s", (limit,))
                return cursor.fetchall()
        finally:
            DBContext.release_connection(conn)

    def get_by_id(self, category_id: int):
        conn = DBContext.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM categories WHERE id = %s", (category_id,))
                return cursor.fetchone()
        finally:
            DBContext.release_connection(conn)

    def get_main_categories(self, limit: int = 100):
        conn = DBContext.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM categories WHERE parent_id IS NULL OR level = 1 ORDER BY name LIMIT %s", (limit,))
                return cursor.fetchall()
        finally:
            DBContext.release_connection(conn)

    def get_closest(self, vector: list[float], limit: int = 10):
        conn = DBContext.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                vector_str = "[" + ",".join(map(str, vector)) + "]"
                query = """
                SELECT id, name, level, full_path, trendyol_cat_id, is_leaf, parent_id,
                       1 - (embedding <=> %s::vector) AS similarity
                FROM categories
                WHERE embedding IS NOT NULL
                ORDER BY embedding <=> %s::vector
                LIMIT %s
                """
                cursor.execute(query, (vector_str, vector_str, limit))
                return cursor.fetchall()
        finally:
            DBContext.release_connection(conn)
