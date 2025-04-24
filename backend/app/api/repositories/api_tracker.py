from fastapi import Depends, HTTPException, status
from redis.asyncio import Redis
import time

from app.api.models import AdminUsers, User
from app.core.databases.redis import get_redis_connection_api_traffic_db as rdb


class APITracker:
    def __init__(self, redis_client: Redis = Depends(rdb)):
        self.__redis_client: Redis = redis_client
        self.rate_limit = 5
        self.decay_rate = 100

    async def __increment_api_call_count(self, key: str) -> int:
        return await self.__redis_client.incr(key)

    async def __get_api_call_count(self, key: str) -> int:
        value = await self.__redis_client.get(key)
        return int(value) if value else 0

    async def __apply_decay(self, key: str, last_decay_key: str) -> None:
        current_time = int(time.time())
        last_decay_time = await self.__redis_client.get(last_decay_key)
        last_decay_time = int(last_decay_time) if last_decay_time else current_time

        seconds_elapsed = current_time - last_decay_time

        if seconds_elapsed > 0:
            current_count = await self.__get_api_call_count(key)
            tokens_to_remove = min(current_count, self.decay_rate * seconds_elapsed)

            if tokens_to_remove > 0:
                new_count = max(0, current_count - tokens_to_remove)
                await self.__redis_client.set(key, new_count)

            await self.__redis_client.set(last_decay_key, current_time)

    async def check_user_api_calls(self, user: AdminUsers | User) -> None:
        # if isinstance(user, AdminUsers):
        #     return None
        key = f"user:{user.telegram_id}:api_calls"
        last_decay_key = f"user:{user.telegram_id}:last_decay"

        await self.__apply_decay(key, last_decay_key)
        current_calls = await self.__increment_api_call_count(key)
        if current_calls == 1:
            await self.__redis_client.expire(key, 60
            )
            await self.__redis_client.expire(last_decay_key, 60)
        if current_calls > self.rate_limit:
            excess_calls = current_calls - self.rate_limit
            retry_after = (excess_calls // self.decay_rate) + 1

            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Try again in {retry_after} seconds.",
                headers={"Retry-After": str(retry_after)},
            )
        return None
