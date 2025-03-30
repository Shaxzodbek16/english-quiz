import asyncio

from faker import Faker
from sqlalchemy import text

from app.api.utils.admins import hash_password
from app.core.databases.postgres import get_session_without_depends
from app.api.models.admins import AdminUsers
from app.core.settings import get_settings, Settings

settings: Settings = get_settings()
fake = Faker()


async def get_admin_by_telegram_id(telegram_id: int) -> bool:
    async with get_session_without_depends() as session:
        admin = await session.execute(
            text("SELECT * FROM admins WHERE telegram_id = :telegram_id"),
            {"telegram_id": telegram_id},
        )
        return admin.scalars().first() is not None


async def create_super_user() -> bool:
    try:
        for telegram_id in settings.get_superusers:
            if await get_admin_by_telegram_id(telegram_id):
                continue
            async with get_session_without_depends() as session:
                admin = AdminUsers(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.email(),
                    password=hash_password("12345678"),
                    is_admin=True,
                    is_superuser=True,
                    telegram_id=telegram_id,
                )
                session.add(admin)
                await session.commit()
        return True
    except Exception as e:
        print(f"Error creating superuser: {e}")
        return False


if __name__ == "__main__":
    asyncio.run(create_super_user())
