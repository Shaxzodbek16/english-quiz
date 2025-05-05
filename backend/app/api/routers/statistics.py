from fastapi import APIRouter, Depends, status, Query

from app.api.controllers.statistics import StatisticsController
from app.api.models import AdminUsers, User
from app.api.schemas.statistics import YearlyUsersResponseModel, DashboardResponseModel
from app.api.utils.admins import get_current_user

router = APIRouter(
    prefix="/statistics",
    tags=["User statistics"],
    redirect_slashes=False,
)


@router.get(
    "/dashboard/",
    response_model=DashboardResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Get dashboard statistics",
    description="Get dashboard statistics",
)
async def get_dashboard_statistics(
    statistics_controller: StatisticsController = Depends(),
    current_user: AdminUsers | User = Depends(get_current_user),
) -> DashboardResponseModel:
    return await statistics_controller.get_dashboard_statistics(
        current_user=current_user
    )


@router.get(
    "/yearly/",
    response_model=YearlyUsersResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Get yearly statistics",
    description="Get yearly statistics",
)
async def get_yearly_statistics(
    year: int | None = Query(None, description="Year to get statistics for"),
    statistics_controller: StatisticsController = Depends(),
    current_user: AdminUsers | User = Depends(get_current_user),
) -> YearlyUsersResponseModel:
    return await statistics_controller.get_yearly_statistics(
        year=year,
        current_user=current_user,
    )


@router.get(
    "/xlsx/",
    status_code=status.HTTP_200_OK,
    summary="Get XLSX statistics",
    description="Get XLSX statistics",
)
async def get_xlsx_statistics(
    statistics_controller: StatisticsController = Depends(),
    current_user: AdminUsers | User = Depends(get_current_user),
):
    return await statistics_controller.get_xlsx_statistics(current_user=current_user)
