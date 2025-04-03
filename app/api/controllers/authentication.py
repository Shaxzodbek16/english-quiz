from fastapi import Depends, HTTPException, status

from app.api.repositories.admins import AdminRepository
from app.api.repositories.users import UserRepository
from app.api.schemas.authentication import AdminLoginSchema, TokenResponseSchema
from app.api.utils.admins import jwt_handler
from app.api.utils.admins import verify_password
from app.api.utils.security import get_telegram_id


class AuthenticationController:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        admin_repository: AdminRepository = Depends(),
    ):
        self.__user_repository = user_repository
        self.__admin_repository = admin_repository
        self.__token_handler = jwt_handler

    @staticmethod
    async def __verify_password(password: str, plain_password: str) -> None:
        if not verify_password(password, plain_password):
            raise HTTPException(
                detail="Email or password is incorrect",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

    async def admin_login(self, data: AdminLoginSchema) -> TokenResponseSchema:
        if isinstance(data.telegram_id_or_email, str):
            admin_user = await self.__admin_repository.get_admin_by_email(
                data.telegram_id_or_email
            )
            if admin_user is None:
                raise HTTPException(
                    detail="Email or password is incorrect",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )
            await self.__verify_password(str(data.password), str(admin_user.password))
            return TokenResponseSchema(
                access_token=self.__token_handler.create_access_token(
                    admin_user.to_dict()
                ),
                refresh_token=self.__token_handler.create_refresh_token(
                    admin_user.to_dict()
                ),
            )
        if isinstance(data.telegram_id_or_email, int):
            admin_user = await self.__admin_repository.get_admin_by_telegram_id(
                data.telegram_id_or_email
            )
            if admin_user is None:
                raise HTTPException(
                    detail="Telegram ID or password is incorrect",
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )
            await self.__verify_password(str(data.password), str(admin_user.password))
            return TokenResponseSchema(
                access_token=self.__token_handler.create_access_token(
                    admin_user.to_dict()
                ),
                refresh_token=self.__token_handler.create_refresh_token(
                    admin_user.to_dict()
                ),
            )
        raise HTTPException(
            detail="Telegram ID or email is incorrect",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    async def user_login(self, *, telegram_id_hash: str) -> TokenResponseSchema:
        telegram_id = get_telegram_id(telegram_id_hash)
        user = await self.__user_repository.get_user_by_telegram_id(telegram_id)
        if user is None:
            raise HTTPException(
                detail="Telegram ID is incorrect",
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        return TokenResponseSchema(
            access_token=self.__token_handler.create_access_token(user.to_dict()),
            refresh_token=self.__token_handler.create_refresh_token(user.to_dict()),
        )
