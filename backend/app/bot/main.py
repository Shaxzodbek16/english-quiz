import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.core.settings import get_settings, Settings
from app.bot.routers import v1_router
from app.core.middlewares.language import I18nMiddleware
from app.core.middlewares.throttling import ThrottlingMiddleware

settings: Settings = get_settings()
dp = Dispatcher()
bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)


async def main() -> None:

    throttling_middleware = ThrottlingMiddleware(limit_time=1, limit_count=2)

    i18n_middleware = I18nMiddleware()
    dp.message.middleware(i18n_middleware)
    dp.callback_query.middleware(i18n_middleware)
    dp.update.middleware(throttling_middleware)

    dp.include_router(v1_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        logging.basicConfig(level=logging.INFO, stream=sys.stdout)
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot foydalanuvchi tomonidan to'xtatildi")
    except Exception as error:
        logging.error(f"Xatolik yuz berdi: {error}")
        logging.info("Bot xatolik tufayli to'xtatildi")
