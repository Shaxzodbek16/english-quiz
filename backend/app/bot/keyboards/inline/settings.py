from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_settings_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌍 Languages", callback_data="settings_language"
                ),
                InlineKeyboardButton(
                    text="🔔 Notifications", callback_data="settings_notification"
                ),
            ],
            [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_main")],
        ]
    )
    return keyboard
