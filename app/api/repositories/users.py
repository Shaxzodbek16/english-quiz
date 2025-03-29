from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.core.databases.postgres import get_general_session


class UserRepository:
    def __init__(
            self,
            session: AsyncSession = Depends(get_general_session),
    ):
        self.__session = session
