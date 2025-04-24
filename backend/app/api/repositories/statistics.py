from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy import select, func, extract
from datetime import datetime, timedelta, timezone

from app.api.schemas.statistics import YearlyType, DashboardResponseModel
from app.core.databases.postgres import get_general_session
from app.api.models import User


class StatisticsRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)):
        self.__session = session

    async def _get_users_by_period(self, period_in_days: int | None = None) -> int:
        stmt = select(func.count()).select_from(User)

        if period_in_days is not None:
            stmt = stmt.where(
                User.created_at >= datetime.now() - timedelta(days=period_in_days)
            )

        result = await self.__session.execute(stmt)
        return result.scalar_one()

    async def _get_avg_users_all_time(self) -> float:
        total_stmt = select(func.count()).select_from(User)
        total_users_result = await self.__session.execute(total_stmt)
        total_users = total_users_result.scalar_one()

        first_user_stmt = select(func.min(User.created_at))
        first_user_result = await self.__session.execute(first_user_stmt)
        first_user_date = first_user_result.scalar_one()

        if not first_user_date:
            return 0.0

        days_elapsed = max((datetime.now(timezone.utc) - first_user_date).days, 1)
        average = total_users / days_elapsed
        return round(average, 2)

    async def get_dashboard_statistics(self) -> DashboardResponseModel:
        return DashboardResponseModel(
            daily_users=await self._get_users_by_period(1),
            weekly_users=await self._get_users_by_period(7),
            monthly_users=await self._get_users_by_period(30),
            total_users=await self._get_users_by_period(365),
            average_daily_users=await self._get_avg_users_all_time(),
        )

    async def get_yearly_statistics(self, *, year: None | int = None) -> YearlyType:
        stmt = (
            select(
                extract("year", User.created_at).label("year"),
                extract("month", User.created_at).label("month"),
                func.count().label("users_count"),
            )
            .group_by("year", "month")
            .order_by("year", "month")
        )

        result = await self.__session.execute(stmt)
        rows = result.all()

        stats: YearlyType = {}

        for row in rows:
            y, m, count = int(row.year), int(row.month), row.users_count

            if y not in stats:
                stats[y] = {}

            stats[y][m] = count
        if year is not None:
            return {year: stats.get(year, {})}
        return stats
