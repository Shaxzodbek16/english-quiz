from app.api.models import AdminUsers, User
from app.api.repositories.options import OptionsRepository
from app.api.repositories.tests import TestsRepository
from app.api.repositories.user_tests import UserTestRepository
from app.api.repositories.users import UserRepository
from app.api.schemas.user_tests import UserTestResponseSchema, UserTestCreateSchema

from fastapi import Depends, HTTPException


class UserTestController:

    def __init__(
        self,
        user_test_repository: UserTestRepository = Depends(),
        user_repository: UserRepository = Depends(),
        options_repository: OptionsRepository = Depends(),
        tests_repository: TestsRepository = Depends(),
    ) -> None:
        self.__user_test_repository: UserTestRepository = user_test_repository
        self.__user_repository: UserRepository = user_repository
        self.__options_repository: OptionsRepository = options_repository
        self.__tests_repository: TestsRepository = tests_repository

    async def __is_valid(
        self, /, *, test_id: int, selected_option_id: int, correct_option_id: int
    ) -> None:
        test = await self.__tests_repository.get_test_by_id(test_id=test_id)
        if not test:
            raise HTTPException(status_code=404, detail="Test not found")
        option = await self.__options_repository.get_option_by_id(
            option_id=selected_option_id
        )
        if not option:
            raise HTTPException(status_code=404, detail="Option not found")
        coid = await self.__options_repository.get_option_by_id(
            option_id=correct_option_id
        )
        if not coid:
            raise HTTPException(status_code=404, detail="Correct option not found")

    async def create_user_test(
        self,
        *,
        data: UserTestCreateSchema,
        user: User | AdminUsers,
    ) -> UserTestResponseSchema:
        await self.__is_valid(
            test_id=data.test_id,
            selected_option_id=data.selected_option_id,
            correct_option_id=data.correct_option_id,
        )

        res = await self.__user_test_repository.create_user_test(
            data=data, user_id=user.get_id()
        )

        return UserTestResponseSchema.model_validate(res)

    async def get_user_test_by_id(
        self, *, user_test_id: int, user: User | AdminUsers
    ) -> UserTestResponseSchema:
        if not await self.__user_repository.get_user_by_id(user.get_id()):
            raise HTTPException(status_code=404, detail="User not found")
        res = await self.__user_test_repository.get_user_test_by_id(
            user_test_id=user_test_id, user_id=user.get_id()
        )
        if not res:
            raise HTTPException(status_code=404, detail="User test not found")
        return UserTestResponseSchema.model_validate(res)

    async def get_all_user_tests(
        self, *, page: int, size: int, user: User | AdminUsers
    ) -> list[UserTestResponseSchema]:
        if not await self.__user_repository.get_user_by_id(user.get_id()):
            raise HTTPException(status_code=404, detail="User not found")
        res = await self.__user_test_repository.get_all_user_tests(
            user_id=user.get_id(), page=page, size=size
        )
        return [UserTestResponseSchema.model_validate(r) for r in res]
