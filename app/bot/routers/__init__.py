from aiogram import Router

v1_router = Router()
from app.bot.routers.start import router as start_router
from app.bot.routers.settings import router as settings_router

v1_router.include_router(start_router)
v1_router.include_router(settings_router)

__all__ = ["v1_router"]
