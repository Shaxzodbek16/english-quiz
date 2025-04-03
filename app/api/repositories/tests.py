from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.databases.postgres import get_general_session


class TestsRepository:
    def __init__(self, session: AsyncSession = Depends(get_general_session)) -> None:
        self.__session: AsyncSession = session
