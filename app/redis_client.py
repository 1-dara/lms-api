import redis
import os

redis_client = redis.Redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379"),
    decode_responses=True
)


def get_cache(key: str):
    try:
        return redis_client.get(key)
    except Exception:
        return None


def set_cache(key: str, value: str, expire: int = 300):
    try:
        redis_client.setex(key, expire, value)
    except Exception:
        pass


def delete_cache(key: str):
    try:
        redis_client.delete(key)
    except Exception:
        pass


def delete_pattern(pattern: str):
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
    except Exception:
        pass
