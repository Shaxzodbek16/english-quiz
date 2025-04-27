import time
from collections import deque
from typing import Callable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit_time: int = 1, limit_count: int = 2):
        self.limit_time = limit_time
        self.limit_count = limit_count
        self.requests: Dict[int, deque] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Any],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user_id = data["event_from_user"].id if data.get("event_from_user") else None
        if user_id:
            now = time.time()
            user_requests = self.requests.setdefault(user_id, deque())

            while user_requests and now - user_requests[0] > self.limit_time:
                user_requests.popleft()

            if len(user_requests) >= self.limit_count:
                return
            user_requests.append(now)
        return await handler(event, data)
