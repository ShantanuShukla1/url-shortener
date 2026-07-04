import redis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def get_cached_url(short_code: str):
    return redis_client.get(short_code)

def set_cached_url(short_code: str, original_url: str, ttl: int = 3600):
    redis_client.set(short_code, original_url, ex=ttl)