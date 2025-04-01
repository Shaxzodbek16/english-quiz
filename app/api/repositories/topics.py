from fastapi import HTTPException, Depends
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.schemas.topics import (
    ResponseTopicSchema,
    CreateTopicSchema,
    UpdateTopicSchema,
)
from app.core.databases.postgres import get_general_session
from app.api.models.topics import Topic


class TopicRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.__session = session

    async def get_all_topics(self) -> Sequence[ResponseTopicSchema]:
        result = await self.__session.execute(select(Topic))
        topics = result.scalars().all()
        return [ResponseTopicSchema.model_validate(topic) for topic in topics]

    async def get_topic_by_id(self, topic_id: int) -> ResponseTopicSchema | None:
        result = await self.__session.execute(select(Topic).where(Topic.id == topic_id))
        topic = result.scalar_one_or_none()
        if topic is None:
            return None
        return ResponseTopicSchema.model_validate(topic)

    async def get_topic_by_name(self, name: str) -> int:
        result = await self.__session.execute(select(Topic).where(Topic.name == name))
        return len(result.scalars().all())

    async def create_topic(self, topic: CreateTopicSchema) -> ResponseTopicSchema:
        new_topic = Topic(**topic.model_dump())
        self.__session.add(new_topic)
        await self.__session.commit()
        await self.__session.refresh(new_topic)
        return ResponseTopicSchema.model_validate(new_topic)

    async def update_topic(
        self, topic: UpdateTopicSchema, topic_id: int
    ) -> ResponseTopicSchema:
        result = await self.__session.execute(select(Topic).where(Topic.id == topic_id))
        existing_topic = result.scalars().first()
        if not existing_topic:
            raise HTTPException(
                status_code=404, detail=f"Topic with id {topic_id} not found"
            )
        for key, value in topic.model_dump().items():
            setattr(existing_topic, key, value)
        await self.__session.commit()
        await self.__session.refresh(existing_topic)
        return ResponseTopicSchema.model_validate(existing_topic)

    async def delete_topic(self, topic_id: int) -> None:
        result = await self.__session.execute(select(Topic).where(Topic.id == topic_id))
        topic = result.scalar_one_or_none()
        if topic is None:
            raise HTTPException(
                status_code=404,
                detail=f"Topic with id {topic_id} not found",
            )
        await self.__session.delete(topic)
        await self.__session.commit()
