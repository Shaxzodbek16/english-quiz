from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    await message.answer("Welcome! I'm your bot. How can I assist you today?")
