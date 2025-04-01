from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.bot.constants.main import start_text, help_text
from app.bot.controllers.users import create_user
from app.bot.keyboards.inlinne.main import InlineKeyboard

router = Router()


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    from_user = message.from_user
    if from_user is None:
        return
    button = InlineKeyboard(message=message)
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
        await message.answer(start_text.format(from_user.first_name))
    await message.answer(
        "Let’s get started! 🎯Choose an option below:",
        reply_markup=await button.start_command_reply_markup(),
    )


@router.message(Command("help"))
async def show_help(message: Message):
    from_user = message.from_user
    if from_user is None:
        return
    await message.answer(help_text.format(from_user.first_name))
