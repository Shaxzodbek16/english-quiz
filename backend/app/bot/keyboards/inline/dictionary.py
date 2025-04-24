from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


def get_dictionaries_menu() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌐 Google Translate",
                    web_app=WebAppInfo(url="https://translate.google.com/"),
                ),
                InlineKeyboardButton(
                    text="📘 Cambridge Dictionary",
                    web_app=WebAppInfo(url="https://dictionary.cambridge.org/"),
                ),
            ],
            [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_main")],
        ]
    )
    return keyboard


def back_to_main() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Back", callback_data="back_to_main")]
        ]
    )
