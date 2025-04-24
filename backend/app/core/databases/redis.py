from functools import cache
from typing import AsyncGenerator

import redis.asyncio as redis
from app.core.settings import get_settings

settings = get_settings()


@cache
def get_redis_pool(database: int):
    return redis.ConnectionPool.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{database}",
        encoding="utf-8",
        decode_responses=True,
        max_connections=10,
    )


async def get_redis_connection_api_traffic_db() -> AsyncGenerator[redis.Redis, None]:
    pool = get_redis_pool(settings.API_TRAFFIC_DB)
    conn = redis.Redis(connection_pool=pool)
    try:
        yield conn
    finally:
        await conn.aclose()


async def get_redis_connection_cache_db() -> AsyncGenerator[redis.Redis, None]:
    pool = get_redis_pool(settings.CACHE_DB)
    conn = redis.Redis(connection_pool=pool)
    try:
        yield conn
    finally:
        await conn.aclose()
