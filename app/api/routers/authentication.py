from fastapi import Depends, APIRouter, status

from app.api.controllers.authentication import AuthenticationController
from app.api.schemas.authentication import LoginSchema, TokenResponseSchema
from app.core.settings import get_settings, Settings

settings: Settings = get_settings()

router = APIRouter(
    prefix=settings.API_V1_STR + "/admin/authentication",
    tags=["Admin authentication"],
    redirect_slashes=False,
)


@router.post(
    "/login/",
    response_model=TokenResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def login(
    data: LoginSchema,
    authentication_controller: AuthenticationController = Depends(),
) -> TokenResponseSchema:
    return await authentication_controller.login(data)
