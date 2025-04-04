from fastapi import Depends, APIRouter, status
from typing import Sequence

from app.api.models import AdminUsers, User
from app.api.schemas.test_types import (
    TestTypeResponseSchema,
    TestTypeCreateSchema,
    TestTypeUpdateSchema,
)
from app.api.constants.test_types.docs import DOCS
from app.api.utils.admins import get_current_user
from app.api.controllers.test_types import TestTypesController

router = APIRouter(
    prefix="/test_types",
    tags=["Test types"],
    redirect_slashes=False,
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Sequence[TestTypeResponseSchema],
    summary=DOCS["get_all"]["summary"],
    description=DOCS["get_all"]["description"],
)
async def get_all_test_types(
    current_user: AdminUsers | User = Depends(get_current_user),  # noqa
    test_types_controller: TestTypesController = Depends(),
) -> Sequence[TestTypeResponseSchema]:
    return await test_types_controller.get_all_test_types()


@router.get(
    "/{test_type_id}/",
    status_code=status.HTTP_200_OK,
    response_model=TestTypeResponseSchema,
    summary=DOCS["get"]["summary"],
    description=DOCS["get"]["description"],
)
async def get_test_type_by_id(
    test_type_id: int,
    current_user: AdminUsers | User = Depends(get_current_user),  # noqa
    test_types_controller: TestTypesController = Depends(),
) -> TestTypeResponseSchema:
    return await test_types_controller.get_test_type_by_id(test_type_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=TestTypeResponseSchema,
    summary=DOCS["create"]["summary"],
    description=DOCS["create"]["description"],
)
async def create_test_type(
    test_type: TestTypeCreateSchema,
    current_user: AdminUsers | User = Depends(get_current_user),  # noqa
    test_types_controller: TestTypesController = Depends(),
) -> TestTypeResponseSchema:
    return await test_types_controller.create_test_type(
        user=current_user, test_type=test_type
    )


@router.put(
    "/{test_type_id}/",
    status_code=status.HTTP_200_OK,
    response_model=TestTypeResponseSchema,
    summary=DOCS["update"]["summary"],
    description=DOCS["update"]["description"],
)
async def update_test_type(
    test_type_id: int,
    test_type: TestTypeUpdateSchema,
    current_user: AdminUsers | User = Depends(get_current_user),  # noqa
    test_types_controller: TestTypesController = Depends(),
) -> TestTypeResponseSchema:
    return await test_types_controller.update_test_type(
        test_type_id=test_type_id, user=current_user, test_type=test_type
    )


@router.delete(
    "/{test_type_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary=DOCS["delete"]["summary"],
    description=DOCS["delete"]["description"],
)
async def delete_test_type(
    test_type_id: int,
    current_user: AdminUsers | User = Depends(get_current_user),  # noqa
    test_types_controller: TestTypesController = Depends(),
) -> None:
    await test_types_controller.delete_test_type(
        test_type_id=test_type_id, user=current_user
    )
