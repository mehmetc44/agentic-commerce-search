from context.DBContext import DBContext
from psycopg2.extras import RealDictCursor

class ProductRepository:
    def get_all(self, limit: int = 100):
        conn = DBContext.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM products LIMIT %s", (limit,))
                return cursor.fetchall()
        finally:
            DBContext.release_connection(conn)

    def get_by_id(self, product_id: int):
        conn = DBContext.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
                return cursor.fetchone()
        finally:
            DBContext.release_connection(conn)
