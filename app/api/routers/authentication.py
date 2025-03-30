from fastapi import Depends, APIRouter, status, Query

from app.api.controllers.authentication import AuthenticationController
from app.api.schemas.authentication import AdminLoginSchema, TokenResponseSchema

admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin Authentication"],
)


@admin_router.post(
    "/login/",
    response_model=TokenResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def admin_login(
    data: AdminLoginSchema,
    authentication_controller: AuthenticationController = Depends(),
) -> TokenResponseSchema:
    return await authentication_controller.admin_login(data)


# # # # # # # # # # # # # # #
#    User Authentication    #
# # # # # # # # # # # # # # #

user_router = APIRouter(
    prefix="/user",
    tags=["User Authentication"],
    redirect_slashes=False,
)


@user_router.post(
    "/login/",
    response_model=TokenResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def user_login(
    user: str = Query(
        ..., title="Telegram ID hash", description="Telegram ID hash of the user"
    ),
    authentication_controller: AuthenticationController = Depends(),
) -> TokenResponseSchema:
    return await authentication_controller.user_login(telegram_id_hash=user)
