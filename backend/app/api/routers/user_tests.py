from fastapi import Depends, APIRouter, Query, status


from app.api.controllers.user_tests import UserTestController
from app.api.models import AdminUsers, User
from app.api.schemas.user_tests import UserTestCreateSchema, UserTestResponseSchema
from app.api.utils.admins import get_current_user


router = APIRouter(
    prefix="/user-tests",
    tags=["user-tests"],
    redirect_slashes=False,
)


@router.post(
    "/",
    response_model=UserTestResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user test",
    description="Create a user test",
)
async def create_user_test(
    data: UserTestCreateSchema,
    current_user: User | AdminUsers = Depends(get_current_user),
    user_test_controller: UserTestController = Depends(),
) -> UserTestResponseSchema:
    return await user_test_controller.create_user_test(data=data, user=current_user)


@router.get(
    "/{user_test_id}/",
    response_model=UserTestResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get a user test by ID",
    description="Get a user test by ID",
)
async def get_user_test_by_id(
    user_test_id: int,
    current_user: User | AdminUsers = Depends(get_current_user),
    user_test_controller: UserTestController = Depends(),
) -> UserTestResponseSchema:
    return await user_test_controller.get_user_test_by_id(
        user_test_id=user_test_id, user=current_user
    )


@router.get(
    "/",
    response_model=list[UserTestResponseSchema],
    status_code=status.HTTP_200_OK,
    summary="Get all user tests",
    description="Get all user tests",
)
async def get_all_user_tests(
    page: int = Query(0, ge=0, description="Page number"),
    size: int = Query(15, ge=1, le=100, description="Page size"),
    current_user: User | AdminUsers = Depends(get_current_user),
    user_test_controller: UserTestController = Depends(),
) -> list[UserTestResponseSchema]:
    return await user_test_controller.get_all_user_tests(
        page=page, size=size, user=current_user
    )
