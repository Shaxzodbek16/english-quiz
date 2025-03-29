from fastapi import Depends, APIRouter, HTTPException, status
from app.core.settings import get_settings, Settings

settings: Settings = get_settings()

router = APIRouter(
    prefix=settings.API_V1_STR + "/admin/authentication",
    tags=["Admin authentication"],
    redirect_slashes=False,
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Authentication credentials were not provided or are invalid."
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "You do not have permission to access this resource."
        },
    },
)
