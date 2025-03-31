from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="EnglishTest", callback_data="test")],
        [
            InlineKeyboardButton(
                text="Google translate",
                web_app=WebAppInfo(url="https://translate.google.com"),
            )
        ],
        [InlineKeyboardButton(text="Settings", callback_data="settings")],
    ]
)
