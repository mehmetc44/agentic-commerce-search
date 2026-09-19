from context.DBContext import DBContext
from psycopg2.extras import RealDictCursor

class ReviewRepository:
    def get_by_product_id(self, product_id: int):
        conn = DBContext.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM reviews WHERE product_id = %s", (product_id,))
                return cursor.fetchall()
        finally:
            DBContext.release_connection(conn)
