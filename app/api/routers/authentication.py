from fastapi import Depends, APIRouter, HTTPException, status
from app.core.settings import get_settings, Settings

settings: Settings = get_settings()

router = APIRouter(
    prefix=settings.API_V1_STR + "/admin/authentication/",
    tags=["Admin authentication"],
    redirect_slashes=False,
)


@router.post("login/")
async def admin_login():
    pass
