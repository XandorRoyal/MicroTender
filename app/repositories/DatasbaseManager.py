from contextlib import asynccontextmanager
from typing import Generic, TypeVar
from asyncpg import create_pool
from asyncpg.exceptions import PostgresConnectionError, PostgresError
from fastapi.params import Depends

from app.settings import get_settings

T = TypeVar('T')

class DatabaseManager:
    _instance = None

    @classmethod
    def depends_init(cls, settings = Depends(get_settings)):
        if cls._instance is None:
            cls._instance = cls(settings)
        return cls._instance

    def __init__(self, settings):
        self.settings = settings
        self.pool = None

    async def init_pool(self):
        self.pool = await create_pool(
            user=self.settings.DB_USER,
            password=self.settings.DB_PASSWORD,
            database=self.settings.DB_NAME,
            host=self.settings.DB_HOST,
            port=self.settings.DB_PORT,
            min_size=self.settings.DB_MIN_POOL_SIZE or 9,
            max_size=self.settings.DB_MAX_POOL_SIZE or 10
        )

    @asynccontextmanager
    async def get_connection(self):
        try:
            if not self.pool:
                await self.init_pool()
            async with self.pool.acquire() as connection:
                yield connection
        except PostgresConnectionError as e:
            print(f"Database connection error: {e}")
            raise ValueError("Unable to connect to the database")
        except PostgresError as e:
            print(f"Database error: {e}")
            raise 

    async def fetchone(self, query: str, filter: list, model: Generic[T]):
        async with self.get_connection() as conn:
            result = await conn.fetchrow(query, *filter)
            return model(**dict(result)) if result else None

    async def execute(self, query: str, filter: list):
        async with self.get_connection() as conn:
            await conn.execute(query, *filter)