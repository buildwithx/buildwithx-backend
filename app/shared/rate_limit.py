from redis.asyncio import Redis


class RateLimiter:
    def __init__(
        self,
        redis: Redis,
    ) -> None:
        self.redis = redis

    async def is_allowed(
        self,
        *,
        key: str,
        limit: int,
        ttl: int,
    ) -> bool:
        current = await self.redis.incr(key)

        if current == 1:
            await self.redis.expire(key, ttl)

        return current <= limit


# -----------------------------------------
# Example usage:
# ```
# allowed = await limiter.is_allowed(
#    key=f"login:{client_ip}",
#    limit=5,
#    ttl=60,
# )
# ```
# -----------------------------------------
