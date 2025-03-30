from fastapi import Depends, APIRouter, HTTPException, status
from app.core.settings import get_settings, Settings

settings: Settings = get_settings()

router = APIRouter(
    prefix="/admins",
    tags=["Admins"],
    redirect_slashes=False,
)
