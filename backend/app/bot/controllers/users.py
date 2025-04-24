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
    new_user = message.from_user
    if new_user is None:
        raise ValueError("User not found in the message")
    exist_user = await get_user_by_telegram_id(new_user.id)  # type: ignore
    if exist_user is not None:
        return exist_user, True
    user = User(
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        telegram_id=new_user.id,
        language=(
            new_user.language_code
            if new_user.language_code in ["en", "uz", "ru"]
            else "en"
        ),
        is_active=True,
    )
    async with get_session_without_depends() as session:
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user, False


async def update_user_language(telegram_id: int, language: str) -> None:
    async with get_session_without_depends() as session:
        user = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        new_user = user.scalar_one_or_none()
        if new_user:
            new_user.language = language
            await session.commit()
