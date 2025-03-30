from fastapi import APIRouter

from app.core.settings import get_settings, Settings

settings: Settings = get_settings()

v1_base_router = APIRouter(
    redirect_slashes=False,
    prefix=settings.API_V1_STR,
)

from app.api.routers.admins import router as admin_router
from app.api.routers.authentication import admin_router as admin_auth_router
from app.api.routers.authentication import user_router as user_auth_router
from app.api.routers.levels import router as levels_router
from app.api.routers.options import router as options_router
from app.api.routers.tests import router as tests_router
from app.api.routers.topics import router as topics_router
from app.api.routers.user_statistics import router as user_statistics_router
from app.api.routers.user_tests import router as user_tests_router
from app.api.routers.users import router as users_router
from app.api.routers.content import router as content_router

v1_base_router.include_router(admin_router)
v1_base_router.include_router(admin_auth_router)
v1_base_router.include_router(user_auth_router)
v1_base_router.include_router(levels_router)
v1_base_router.include_router(options_router)
v1_base_router.include_router(tests_router)
v1_base_router.include_router(topics_router)
v1_base_router.include_router(user_statistics_router)
v1_base_router.include_router(user_tests_router)
v1_base_router.include_router(users_router)
v1_base_router.include_router(content_router)

__all__ = [
    "v1_base_router",
]
