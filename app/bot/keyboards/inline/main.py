from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
    Message,
)

from app.api.models import AdminUsers
from app.bot.controllers.admins import get_user_by_telegram_id
from app.core.settings import get_settings, Settings

settings: Settings = get_settings()


class InlineKeyboard:
    def __init__(self, *, message: Message) -> None:
        self.__message: Message = message

    async def _check_is_admin(self) -> AdminUsers | None:
        from_user = self.__message.from_user
        if from_user is None:
            raise ValueError("User not found in the message")
        admin_user = await get_user_by_telegram_id(from_user.id)
        if admin_user is not None:
            return admin_user
        return None

    async def start_command_reply_markup(self):
        button = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="EnglishTest", callback_data="test")],
                [
                    InlineKeyboardButton(
                        text="Google translate",
                        web_app=WebAppInfo(url="https://translate.google.com"),
                    )
                ],
                [InlineKeyboardButton(text="Settings", callback_data="settings_menu")],
            ]
        )
        admin_user = await self._check_is_admin()
        if admin_user is None:
            return button
        if admin_user.is_superuser:
            button.inline_keyboard.append(
                [
                    InlineKeyboardButton(
                        text="Admin Panel Superuser",
                        url="https://translate.google.com",
                    )
                ],
            )
            return button
        if admin_user.is_admin:
            button.inline_keyboard.append(
                [
                    InlineKeyboardButton(
                        text="Admin Panel",
                        url="https://translate.google.com",
                    )
                ],
            )
        return button
