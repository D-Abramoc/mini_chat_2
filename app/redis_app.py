import redis.asyncio as aioredis


redis = aioredis.from_url(
    "redis://redis", encoding='utf-8', decode_responses=True
)
