from typing import Sequence

from fastapi import Depends, HTTPException, status

from app.api.repositories.levels import LevelRepository
from app.api.repositories.options import OptionsRepository
from app.api.repositories.test_types import TestTypesRepository
from app.api.repositories.tests import TestsRepository
from app.api.repositories.topics import TopicRepository
from app.api.schemas.options import OptionsResponseSchema
from app.api.schemas.tests import TestResponseSchema
from app.api.models import Test


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

    async def get_all_tests(
        self, *, level_id: int, topic_id: int, type_id: int, page: int, size: int
    ) -> Sequence[TestResponseSchema]:
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
        tests: Sequence[Test] = await self.__test_repository.get_all_tests(
            level_id=level_id, topic_id=topic_id, type_id=type_id, page=page, size=size
        )
        result: list[TestResponseSchema] = []
        for test in tests:
            result.append(
                TestResponseSchema(
                    id=test.id,
                    question=test.question,
                    image=test.image,
                    answer_explanation=test.answer_explanation,
                    options=[
                        OptionsResponseSchema.model_validate(
                            (
                                await self.__options_repository.get_option_by_id(
                                    option_id
                                )
                            )
                        )
                        for option_id in test.option_ids
                    ],
                    created_at=test.created_at,
                    updated_at=test.updated_at,
                )
            )
        return result
