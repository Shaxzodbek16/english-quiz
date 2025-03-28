import asyncio
import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.settings import get_settings, Settings
from app.server import create_super_user

from app.api.routers.admins import router as admin_router
from app.api.routers.authentication import router as authentication_router
from app.api.routers.levels import router as levels_router
from app.api.routers.options import router as options_router
from app.api.routers.tests import router as tests_router
from app.api.routers.topics import router as topics_router
from app.api.routers.user_statistics import router as user_statistics_router
from app.api.routers.user_tests import router as user_tests_router
from app.api.routers.users import router as users_router

settings: Settings = get_settings()


def get_ready() -> None:
    os.makedirs("media/", exist_ok=True)
    os.makedirs("static/", exist_ok=True)


def get_app() -> FastAPI:
    get_ready()
    asyncio.create_task(create_super_user())
    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
        docs_url="/",
    )
    app.include_router(admin_router)
    app.include_router(authentication_router)
    app.include_router(levels_router)
    app.include_router(options_router)
    app.include_router(tests_router)
    app.include_router(topics_router)
    app.include_router(user_statistics_router)
    app.include_router(user_tests_router)
    app.include_router(users_router)
    return app


def create_app() -> CORSMiddleware:
    app = get_app()
    return CORSMiddleware(
        app,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
