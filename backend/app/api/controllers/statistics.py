from fastapi import HTTPException, Depends

from app.api.models import AdminUsers, User
from app.api.repositories.statistics import StatisticsRepository
from app.api.repositories.users import UserRepository
from app.api.schemas.statistics import (
    DashboardResponseModel,
    YearlyUsersResponseModel,
    YearlyType,
)
from app.core.tasks import make_file_and_send


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

    @staticmethod
    async def get_xlsx_statistics(current_user: AdminUsers | User):
        if not isinstance(current_user, AdminUsers):
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to access this resource",
            )
        task = make_file_and_send.delay(current_user.telegram_id)
        return {
            "status": "success",
            "task_id": task.id,
            "detail": "XLSX file will be generated and sent to your telegram account",
        }
