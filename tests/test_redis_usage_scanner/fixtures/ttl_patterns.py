from django.core.cache import cache
import redis


def cache_api_patterns(ttl):
    cache.set("user:base", "value", timeout=ttl)
    cache.add("user:add", "value", ttl)
    cache.touch("user:add", ttl)
    cache.delete_many(["user:1", "user:2"])
    cache.clear()
    cache.incr("counter")
    cache.decr("counter")


def direct_redis_patterns(ttl):
    client = redis.Redis()
    client.set("redis:key", "value", ex=ttl)
    client.setex("redis:setex", ttl, "value")
