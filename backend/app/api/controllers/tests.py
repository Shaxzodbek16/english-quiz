from typing import Sequence
from fastapi import Depends, HTTPException, status

from app.api.repositories.levels import LevelRepository
from app.api.repositories.options import OptionsRepository
from app.api.repositories.test_types import TestTypesRepository
from app.api.repositories.tests import TestsRepository
from app.api.repositories.topics import TopicRepository
from app.api.schemas.options import OptionsResponseSchema
from app.api.schemas.tests import TestResponseSchema, TestCreateSchema, TestUpdateSchema
from app.api.models import Test, AdminUsers, User


class TestsController:
    def __init__(
        self,
        test_repository: TestsRepository = Depends(),
        level_repository: LevelRepository = Depends(),
        topic_repository: TopicRepository = Depends(),
        test_types_repository: TestTypesRepository = Depends(),
        options_repository: OptionsRepository = Depends(),
    ) -> None:
        self.__test_repository: TestsRepository = test_repository
        self.__level_repository: LevelRepository = level_repository
        self.__topic_repository: TopicRepository = topic_repository
        self.__test_types_repository: TestTypesRepository = test_types_repository
        self.__options_repository: OptionsRepository = options_repository

    async def __is_valid(self, *, level_id: int, topic_id: int, type_id: int) -> None:
        level = await self.__level_repository.get_level_by_id(level_id)
        if level is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Level not found"
            )
        topic = await self.__topic_repository.get_topic_by_id(topic_id)
        if topic is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found"
            )
        test_type = await self.__test_types_repository.get_test_type_by_id(type_id)
        if test_type is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Test type not found"
            )

    async def get_all_tests(
        self, *, level_id: int, topic_id: int, type_id: int, page: int, size: int
    ) -> list[TestResponseSchema]:
        await self.__is_valid(level_id=level_id, topic_id=topic_id, type_id=type_id)
        tests: Sequence[Test] = await self.__test_repository.get_all_tests(
            level_id=level_id, topic_id=topic_id, type_id=type_id, page=page, size=size
        )
        result: list[TestResponseSchema] = []
        for test in tests:
            result.append(
                TestResponseSchema(
                    **test.to_dict(),
                    options=[
                        OptionsResponseSchema.model_validate(
                            await self.__options_repository.get_option_by_id(option_id)
                        )
                        for option_id in test.option_ids
                    ],
                )
            )
        return result

    async def get_test_by_id(self, test_id: int) -> TestResponseSchema:
        res: Test | None = await self.__test_repository.get_test_by_id(test_id)
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Test not found"
            )
        return TestResponseSchema(
            **res.to_dict(),
            options=[
                OptionsResponseSchema.model_validate(
                    await self.__options_repository.get_option_by_id(option_id)
                )
                for option_id in res.option_ids
            ],
        )

    async def create_test(
        self, *, test: TestCreateSchema, user: User | AdminUsers
    ) -> TestResponseSchema:
        if not isinstance(user, AdminUsers):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
            )
        await self.__is_valid(
            level_id=test.level_id, topic_id=test.topic_id, type_id=test.type_id
        )
        res = await self.__test_repository.create_test(test)
        return TestResponseSchema(
            **res.to_dict(),
            options=[
                OptionsResponseSchema.model_validate(
                    await self.__options_repository.get_option_by_id(option_id)
                )
                for option_id in res.option_ids
            ],
        )

    async def update_test(
        self, *, test_id: int, test: TestUpdateSchema, user: AdminUsers | User
    ) -> TestResponseSchema:
        if not isinstance(user, AdminUsers):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
            )
        if await self.__test_repository.get_test_by_id(test_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Test not found"
            )
        await self.__is_valid(
            level_id=test.level_id, topic_id=test.topic_id, type_id=test.type_id
        )
        res = await self.__test_repository.update_test(test_id=test_id, test=test)
        return TestResponseSchema(
            **res.to_dict(),
            options=[
                OptionsResponseSchema.model_validate(
                    await self.__options_repository.get_option_by_id(option_id)
                )
                for option_id in res.option_ids
            ],
        )

    async def add_option_to_test(
        self, user: User | AdminUsers, test_id: int, option_id: int
    ) -> None:
        if not isinstance(user, AdminUsers):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
            )
        if await self.__test_repository.get_test_by_id(test_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Test not found"
            )
        await self.__options_repository.get_option_by_id(option_id)
        if await self.__options_repository.get_option_by_id(option_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Option not found"
            )
        await self.__test_repository.add_option_to_test(
            test_id=test_id, option_id=option_id
        )

    async def delete_test(self, test_id: int, user: AdminUsers | User) -> None:
        if not isinstance(user, AdminUsers):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
            )
        test = await self.__test_repository.get_test_by_id(test_id)
        if test is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Test not found"
            )
        for option_id in test.option_ids:
            if await self.__options_repository.get_option_by_id(option_id) is None:
                pass
            await self.__options_repository.delete_option(option_id)
        await self.__test_repository.delete_test(test_id=test_id)
