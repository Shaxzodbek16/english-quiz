from fastapi import HTTPException, Depends

from app.api.models import AdminUsers, User
from app.api.repositories.statistics import StatisticsRepository
from app.api.repositories.users import UserRepository
from app.api.schemas.statistics import (
    DashboardResponseModel,
    YearlyUsersResponseModel,
    YearlyType,
)


class StatisticsController:
    def __init__(
        self,
        statistics_repository: StatisticsRepository = Depends(),
        user_repository: UserRepository = Depends(),
    ):
        self.__statistics_repository = statistics_repository
        self.__user_repository = user_repository

    async def get_dashboard_statistics(
        self, current_user: AdminUsers | User
    ) -> DashboardResponseModel:
        if not isinstance(current_user, AdminUsers):
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to access this resource",
            )

        res = await self.__statistics_repository.get_dashboard_statistics()

        return DashboardResponseModel.model_validate(res)

    async def get_yearly_statistics(
        self, *, year: int | None, current_user: AdminUsers | User
    ) -> YearlyUsersResponseModel:
        if not isinstance(current_user, AdminUsers):
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to access this resource",
            )

        res: YearlyType = await self.__statistics_repository.get_yearly_statistics(
            year=year,
        )

        return YearlyUsersResponseModel(data=res)

    async def get_xlsx_statistics(self, current_user: AdminUsers | User):
        if not isinstance(current_user, AdminUsers):
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to access this resource",
            )
        page, limit = 1, 5000
        count = await self.__user_repository.get_users_count()
        # todo : return xlxs file
        return b"1234"
