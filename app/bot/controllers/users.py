from aiogram.types import Message
from sqlalchemy.future import select

from app.api.models.users import User
from app.core.databases.postgres import get_session_without_depends


async def get_user_by_telegram_id(telegram_id: int) -> User | None:
    async with get_session_without_depends() as session:
        user = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return user.scalar_one_or_none()


async def create_user(message: Message) -> tuple[User, bool]:
    exist_use = await get_user_by_telegram_id(message.from_user.id)
    if exist_use is not None:
        return exist_use, True
    user = User(
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        telegram_id=message.from_user.id,
        language=message.from_user.language_code,
        is_active=True,
    )
    async with get_session_without_depends() as session:
        session.add(user)
        await session.commit()
    return user, False
