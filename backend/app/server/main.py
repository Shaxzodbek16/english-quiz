import asyncio
import os
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.settings import get_settings, Settings
from app.server import create_super_user

from app.api.routers import v1_base_router

settings: Settings = get_settings()


def get_ready() -> None:
    os.makedirs("media/uploads/images", exist_ok=True)
    os.makedirs("media/uploads/videos", exist_ok=True)
    os.makedirs("media/uploads/docs", exist_ok=True)
    os.makedirs("static/images", exist_ok=True)
    os.makedirs("static/videos", exist_ok=True)
    os.makedirs("static/docs", exist_ok=True)


def get_app() -> FastAPI:
    get_ready()
    asyncio.create_task(create_super_user())
    app = FastAPI(
        debug=settings.DEBUG,
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
        docs_url="/",
        redoc_url="/redoc",
    )
    app.include_router(v1_base_router)
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
