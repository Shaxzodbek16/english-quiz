from aiogram.filters import BaseFilter
from aiogram.types import Message


from app.bot.controllers.admins import get_admin_by_telegram_id


class SuperUserFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        if message.from_user is None:
            return False
        user = await get_admin_by_telegram_id(message.from_user.id)
        if user is None:
            return False
        return user.is_superuser
