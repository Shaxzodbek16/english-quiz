from fastapi import Depends, HTTPException

from app.api.models import AdminUsers, User
from app.api.repositories.users import UserRepository
from app.api.schemas.users import UserResponseSchema, UserUpdateSchema


class UserController:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.__user_repository = user_repository

    async def get_me(self, current_user: AdminUsers | User) -> UserResponseSchema:
        user = await self.__user_repository.get_user_by_id(current_user.get_id())
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserResponseSchema.model_validate(user)

    async def update_user(
        self, current_user: AdminUsers | User, data: UserUpdateSchema
    ) -> UserResponseSchema:
        user = await self.__user_repository.get_user_by_id(current_user.get_id())
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        new_user = await self.__user_repository.update_user(data, current_user.get_id())
        return UserResponseSchema.model_validate(new_user)
