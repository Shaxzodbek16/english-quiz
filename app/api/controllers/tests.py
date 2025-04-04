from fastapi import Depends

from app.api.repositories.tests import TestsRepository


class TestsController:
    def __init__(self, test_repository: TestsRepository = Depends()) -> None:
        self.__test_repository: TestsRepository = test_repository
