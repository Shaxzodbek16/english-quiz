from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from app.bot.controllers.users import get_user_by_telegram_id, update_user_language
from app.bot.keyboards.inline.language import get_language_keyboard
from app.bot.keyboards.inline.settings import get_settings_menu
from app.core.middlewares.language import I18nMiddleware

router = Router()


async def show_language_selection(
    message: Message, i18n: I18nMiddleware, locale: str
) -> None:
    user = await get_user_by_telegram_id(message.from_user.id)
    if not user:
        from app.bot.controllers.users import create_user

        await create_user(message)
    settings_text = i18n._("settings_message", locale)
    await message.reply(settings_text, reply_markup=get_language_keyboard())


@router.message(F.text == "/settings")
async def settings_command(message: Message, i18n: I18nMiddleware, locale: str) -> None:
    settings_text = i18n._("settings_message", locale)
    await message.reply(settings_text, reply_markup=get_settings_menu())


@router.callback_query(F.data == "settings_menu")
async def settings_menu_callback(
    callback: CallbackQuery, i18n: I18nMiddleware, locale: str
) -> None:
    if callback.message is None:
        return
    settings_text = i18n._("settings_message", locale)
    await callback.message.reply(settings_text, reply_markup=get_settings_menu())
    await callback.answer()


@router.callback_query(F.data == "settings_language")
async def settings_language_callback(
    callback: CallbackQuery, i18n: I18nMiddleware, locale: str
) -> None:
    if callback.message is None:
        return
    await show_language_selection(callback.message, i18n, locale)
    await callback.answer()


@router.callback_query(F.data == "settings_notification")
async def settings_notification_callback(
    callback: CallbackQuery, i18n: I18nMiddleware, locale: str
) -> None:
    if callback.message is None:
        return
    await callback.message.reply("Notification settings are not implemented yet!")
    await callback.answer()


@router.callback_query(F.data.startswith("lang_"))
async def process_language_selection(
    callback: CallbackQuery, i18n: I18nMiddleware, locale: str
) -> None:
    lang = callback.data.split("_")[1]
    user_id = callback.from_user.id

    await update_user_language(user_id, lang)

    locale = await i18n.get_locale(callback, {"event_from_user": callback.from_user})
    confirmation_text = i18n._("language_set", locale, lang=lang.capitalize())

    await callback.message.reply(confirmation_text)
    await callback.answer()
