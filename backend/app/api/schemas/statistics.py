from pydantic import BaseModel, ConfigDict, Field

type YearlyType = dict[int, dict[int, int]]


class DashboardResponseModel(BaseModel):
    daily_users: int
    weekly_users: int
    monthly_users: int
    total_users: int
    average_daily_users: float

    model_config = ConfigDict(from_attributes=True)


class YearlyUsersResponseModel(BaseModel):
    data: YearlyType
    model_config = ConfigDict(from_attributes=True)
