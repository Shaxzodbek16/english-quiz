from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    await message.answer("Welcome! I'm your bot. How can I assist you today?")


@router.message(Command(commands=["help"]))
async def help_command(message: Message) -> None:
    await message.answer(
        "Here are the commands you can use:\n"
        "/start - Start the bot\n"
        "/help - Get help with using the bot\n"
        "/settings - Change your settings"
    )


@router.message(Command(commands=["settings"]))
async def settings_command(message: Message) -> None:
    await message.answer(
        "Here are your settings:\n"
        "1. Notifications: ON\n"
        "2. Language: English\n"
        "You can change these settings in the app."
    )
