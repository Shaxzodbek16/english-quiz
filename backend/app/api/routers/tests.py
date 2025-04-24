from fastapi import Depends, APIRouter, status, Query
from typing import Sequence

from app.api.controllers.tests import TestsController
from app.api.schemas.tests import TestResponseSchema, TestCreateSchema, TestUpdateSchema
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
    current_user: AdminUsers | User = Depends(get_current_user),
    tests_controller: TestsController = Depends(),
) -> Sequence[TestResponseSchema]:
    return await tests_controller.get_all_tests(
        level_id=level_id,
        topic_id=topic_id,
        type_id=type_id,
        page=page,
        size=size,
        current_user=current_user,
    )


@router.get(
    "/{test_id}/",
    status_code=status.HTTP_200_OK,
    response_model=TestResponseSchema,
    summary="Get test by ID",
    description="Returns a test by its ID.",
)
async def get_test_by_id(
    test_id: int,
    current_user: AdminUsers | User = Depends(get_current_user),
    tests_controller: TestsController = Depends(),
) -> TestResponseSchema:
    return await tests_controller.get_test_by_id(test_id, current_user=current_user)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TestResponseSchema,
    summary="Create a new test",
    description="Creates a new test.",
)
async def create_test(
    test: TestCreateSchema,
    current_user: AdminUsers | User = Depends(get_current_user),
    tests_controller: TestsController = Depends(),
) -> TestResponseSchema:
    return await tests_controller.create_test(test=test, user=current_user)


@router.put(
    "/{test_id}/",
    status_code=status.HTTP_200_OK,
    response_model=TestResponseSchema,
    summary="Update a test",
    description="Updates a test by its ID.",
)
async def update_test(
    test_id: int,
    test: TestUpdateSchema,
    current_user: AdminUsers | User = Depends(get_current_user),
    tests_controller: TestsController = Depends(),
) -> TestResponseSchema:
    return await tests_controller.update_test(
        test_id=test_id, test=test, user=current_user
    )


@router.post(
    "/{test_id}/",
)
async def add_option_to_test(
    test_id: int,
    option_id: int,
    current_user: AdminUsers | User = Depends(get_current_user),
    tests_controller: TestsController = Depends(),
) -> None:
    await tests_controller.add_option_to_test(
        test_id=test_id, option_id=option_id, user=current_user
    )


@router.delete(
    "/{test_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a test",
    description="Deletes a test by its ID.",
)
async def delete_test(
    test_id: int,
    current_user: AdminUsers | User = Depends(get_current_user),
    tests_controller: TestsController = Depends(),
):
    await tests_controller.delete_test(test_id=test_id, user=current_user)
