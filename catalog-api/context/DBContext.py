import psycopg2
from psycopg2 import pool
from config import settings
import logging

logger = logging.getLogger(__name__)

class DBContext:
    _pool = None

    @classmethod
    def initialize(cls):
        if cls._pool is None:
            try:
                cls._pool = pool.SimpleConnectionPool(
                    1, 20,
                    dbname=settings.DB_NAME,
                    user=settings.DB_USER,
                    password=settings.DB_PASSWORD,
                    host=settings.DB_HOST,
                    port=settings.DB_PORT
                )
                logger.info("✅ Database connection pool created successfully.")
            except Exception as e:
                logger.error(f"❌ Error creating connection pool: {e}")
                raise e

    @classmethod
    def get_connection(cls):
        if cls._pool is None:
            cls.initialize()
        return cls._pool.getconn()

    @classmethod
    def release_connection(cls, conn):
        if cls._pool is not None and conn is not None:
            cls._pool.putconn(conn)

    @classmethod
    def close_all(cls):
        if cls._pool is not None:
            cls._pool.closeall()
            logger.info("Database connection pool closed.")
