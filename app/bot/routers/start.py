from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.bot.controllers.users import create_user
from app.bot.keyboards.inlinne.main import keyboard

router = Router()


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    try:
        user, is_old = await create_user(message)
    except Exception as e:
        await message.answer(
            "An error occurred while creating your profile. Please try again with /start."
            + str(e)
        )
        return
    if is_old:
        await message.answer("Welcome back! How can I assist you today?")
    else:
        await message.answer(
            f"Hello, {message.from_user.full_name} welcome\nto the English Grammar Test Bot!🎉\n"
            "\n "
            "📚What can I do?\n "
            "✅ Help you improve your English grammar through interactive tests\n "
            "✅ Provide topic-specific and level-based exercises\n "
            "✅ Offer Google Translate support for quick translations\n "
        )
    await message.answer(
        "Let’s get started! 🎯Choose an option below:", reply_markup=keyboard
    )


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
