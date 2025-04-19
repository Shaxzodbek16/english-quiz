from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.bot.controllers.users import create_user
from app.bot.keyboards.inline.main import InlineKeyboard
from app.core.middlewares.language import I18nMiddleware

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, i18n: I18nMiddleware, locale: str) -> None:
    from_user = message.from_user
    if from_user is None:
        return
    button = InlineKeyboard(message=message)

    try:
        user, is_old = await create_user(message)
    except Exception as e:
        error_text = i18n._("error_message", locale, error=str(e))
        await message.answer(error_text)
        return

    if is_old:
        welcome_back_text = i18n._("welcome_back_message", locale)
        await message.answer(welcome_back_text)
    else:
        welcome_text = i18n._("welcome_message", locale, name=from_user.first_name)
        await message.answer(welcome_text)

    start_message = i18n._("start_message", locale)
    await message.answer(
        start_message,
        reply_markup=await button.start_command_reply_markup(),
    )


@router.message(Command("help"))
async def show_help(message: Message, i18n: I18nMiddleware, locale: str) -> None:
    from_user = message.from_user
    if from_user is None:
        return

    help_message = i18n._("help_message", locale, name=from_user.first_name)
    await message.answer(help_message)
