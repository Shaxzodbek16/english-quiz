from fastapi import Depends, APIRouter, HTTPException, status, Query
from typing import Sequence

from app.api.controllers.tests import TestsController
from app.api.schemas.tests import TestResponseSchema
from app.api.models import User, AdminUsers
from app.api.utils.admins import get_current_user

router = APIRouter(
    prefix="/tests",
    tags=["Tests"],
    redirect_slashes=False,
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Sequence[TestResponseSchema],
    summary="Get all tests",
    description="Returns a list of all tests.",
)
async def get_all_tests(
    level_id: int = Query(..., ge=1),
    topic_id: int = Query(..., ge=1),
    type_id: int = Query(..., ge=1),
    page: int = Query(1, ge=1),
    size: int = Query(15, ge=1, le=100),
    # current_user: AdminUsers | User = Depends(get_current_user),  # noqa
    tests_controller: TestsController = Depends(),
) -> Sequence[TestResponseSchema]:
    return await tests_controller.get_all_tests(
        level_id=level_id, topic_id=topic_id, type_id=type_id, page=page, size=size
    )
