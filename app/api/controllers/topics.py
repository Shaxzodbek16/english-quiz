from fastapi import Depends, HTTPException, status
from typing import Sequence

from app.api.models import AdminUsers, User
from app.api.repositories.topics import TopicRepository
from app.api.schemas.topics import (
    ResponseTopicSchema,
    CreateTopicSchema,
    UpdateTopicSchema,
)


class TopicController:
    def __init__(self, topic_repository: TopicRepository = Depends()):
        self.__topic_repository = topic_repository

    async def get_all_topics(self) -> Sequence[ResponseTopicSchema]:
        return [
            ResponseTopicSchema.model_validate(topic)
            for topic in await self.__topic_repository.get_all_topics()
        ]

    async def get_topic_by_id(self, topic_id: int) -> ResponseTopicSchema:
        topic = await self.__topic_repository.get_topic_by_id(topic_id)
        if topic is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Not found",
            )
        return ResponseTopicSchema.model_validate(topic)

    async def create_topic(
        self, topic: CreateTopicSchema, current_user: AdminUsers | User
    ) -> ResponseTopicSchema:
        if isinstance(current_user, User):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized",
            )
        if await self.__topic_repository.get_topic_by_name(topic.name) >= 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Topic with name {topic.name} already exists",
            )
        return ResponseTopicSchema.model_validate(
            await self.__topic_repository.create_topic(topic)
        )

    async def update_topic(
        self,
        *,
        topic: UpdateTopicSchema,
        topic_id: int,
        current_user: AdminUsers | User,
    ) -> ResponseTopicSchema:
        if isinstance(current_user, User):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized",
            )
        if await self.__topic_repository.get_topic_by_name(topic.name) > 2:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Topic with name {topic.name} already exists",
            )

        return ResponseTopicSchema.model_validate(
            await self.__topic_repository.update_topic(topic, topic_id)
        )

    async def delete_topic(
        self, *, topic_id: int, current_user: AdminUsers | User
    ) -> None:
        if isinstance(current_user, User):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized",
            )
        topic = await self.__topic_repository.get_topic_by_id(topic_id)
        if topic is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Topic with id {topic_id} not found",
            )
        return await self.__topic_repository.delete_topic(topic_id)
