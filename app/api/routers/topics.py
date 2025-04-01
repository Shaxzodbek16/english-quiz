from fastapi import Depends, APIRouter, status, Path

from typing import Sequence
from app.api.models import AdminUsers, User
from app.api.utils.admins import get_current_user
from app.api.controllers.topics import TopicController
from app.api.schemas.topics import (
    ResponseTopicSchema,
    CreateTopicSchema,
    UpdateTopicSchema,
)
from app.api.constants.topics.docs import TOPIC_DOCS

router = APIRouter(
    prefix="/topics",
    tags=["Topics"],
    redirect_slashes=False,
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Sequence[ResponseTopicSchema],
    summary=TOPIC_DOCS["get"]["summary"],
    description=TOPIC_DOCS["get"]["description"],
)
async def get_all_topics(
    current_user: AdminUsers | User = Depends(get_current_user),
    topic_controller: TopicController = Depends(),
) -> Sequence[ResponseTopicSchema]:
    return await topic_controller.get_all_topics()


@router.get(
    "/{topic_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseTopicSchema,
    summary=TOPIC_DOCS["get_one"]["summary"],
    description=TOPIC_DOCS["get_one"]["description"],
)
async def get_topic_by_id(
    current_user: AdminUsers | User = Depends(get_current_user),
    topic_id: int = Path(..., ge=1),
    topic_controller: TopicController = Depends(),
) -> ResponseTopicSchema:
    return await topic_controller.get_topic_by_id(topic_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseTopicSchema,
    summary=TOPIC_DOCS["create"]["summary"],
    description=TOPIC_DOCS["create"]["description"],
)
async def create_topic(
    topic: CreateTopicSchema,
    topic_controller: TopicController = Depends(),
    current_user: AdminUsers | User = Depends(get_current_user),
) -> ResponseTopicSchema:
    return await topic_controller.create_topic(topic, current_user)


@router.put(
    "/{topic_id}/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseTopicSchema,
    summary=TOPIC_DOCS["update"]["summary"],
    description=TOPIC_DOCS["update"]["description"],
)
async def update_topic(
    topic: UpdateTopicSchema,
    current_user: AdminUsers | User = Depends(get_current_user),
    topic_id: int = Path(..., ge=1),
    topic_controller: TopicController = Depends(),
) -> ResponseTopicSchema:
    return await topic_controller.update_topic(
        topic=topic, topic_id=topic_id, current_user=current_user
    )


@router.delete(
    "/{topic_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary=TOPIC_DOCS["delete"]["summary"],
    description=TOPIC_DOCS["delete"]["description"],
)
async def delete_topic(
    topic_id: int = Path(..., ge=1),
    topic_controller: TopicController = Depends(),
    current_user: AdminUsers | User = Depends(get_current_user),
) -> None:
    return await topic_controller.delete_topic(
        topic_id=topic_id, current_user=current_user
    )
