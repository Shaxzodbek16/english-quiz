from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_settings_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Language", callback_data="settings_language"
                ),
                InlineKeyboardButton(
                    text="Notification", callback_data="settings_notification"
                ),
            ]
        ]
    )
    return keyboard
