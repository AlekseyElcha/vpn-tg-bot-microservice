from contextlib import asynccontextmanager

from redis.asyncio import Redis

from src.config.settings import settings


@asynccontextmanager
async def get_redis_client():
    client = Redis.from_url(
        f"redis://{settings.redis.host}:{settings.redis.port}",
        decode_responses=True
    )
    try:
        yield client
    finally:
        await client.aclose()