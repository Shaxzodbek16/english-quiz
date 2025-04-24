import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile

from app.api.models import AdminUsers, User
from app.core.settings import get_settings, Settings

settings: Settings = get_settings()
dp = Dispatcher()

bot = Bot(
    token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


async def send_msg2users(*, data: dict[str, list[str]], users: list[AdminUsers | User]):
    """
    Asynchronous function to send a message to multiple users.
    :param data: The message data to be sent.
    :param users: List of users to whom the message will be sent.
    data = {
    files: ['path/to/file1', 'path/to/file2'],
    text: ['Hello, this is a message', 'name', 'another message'], => Hello, this is a message name another message
    pictures: ['path/to/picture1', 'path/to/picture2'],
    videos: ['path/to/video1', 'path/to/video2'],
    }
    """


async def send_xlsx(tg_id: int, file_path: str):
    if not os.path.exists(file_path):
        await bot.send_message(tg_id, "Fayl topilmadi")

    document = FSInputFile(file_path)
    await bot.send_document(
        chat_id=tg_id,
        document=document,
        caption="Salom, bu sizga yuborilgan fayl",
    )
