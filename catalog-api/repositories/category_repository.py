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
