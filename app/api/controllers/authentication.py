from fastapi import Depends

from app.api.repositories.admins import AdminRepository
from app.api.repositories.users import UserRepository
from app.api.schemas.authentication import LoginSchema, TokenResponseSchema


class AuthenticationController:
    def __init__(
        self,
        user_repository: UserRepository = Depends(),
        admin_repository: AdminRepository = Depends(),
    ):
        self.__user_repository = user_repository
        self.__admin_repository = admin_repository

    async def login(self, data: LoginSchema) -> TokenResponseSchema:
        pass
