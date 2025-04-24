from aiogram.types import TelegramObject, User
from typing import Any, Dict, Optional
import importlib


DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ["en", "uz", "ru"]


def load_translations(lang: str) -> Dict[str, str]:
    try:
        module = importlib.import_module(f"app.core.locales.{lang}")
        return module.translations
    except ImportError:
        module = importlib.import_module(f"app.core.locales.{DEFAULT_LANGUAGE}")
        return module.translations


class I18nMiddleware:
    def __init__(self) -> None:
        self.translations: Dict[str, Dict[str, str]] = {}
        for lang in SUPPORTED_LANGUAGES:
            self.translations[lang] = load_translations(lang)

    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        user: Optional[User] = data.get("event_from_user")
        if not user:
            return DEFAULT_LANGUAGE

        from app.bot.controllers.users import get_user_by_telegram_id

        db_user = await get_user_by_telegram_id(user.id)
        if db_user and db_user.language in SUPPORTED_LANGUAGES:
            return db_user.language
        return DEFAULT_LANGUAGE

    def _(self, key: str, locale: str, **kwargs) -> str:
        translations = self.translations.get(
            locale, self.translations[DEFAULT_LANGUAGE]
        )
        message = translations.get(key, key)
        return message.format(**kwargs)

    async def __call__(self, handler, event, data):
        locale = await self.get_locale(event, data)
        data["i18n"] = self
        data["locale"] = locale
        return await handler(event, data)
