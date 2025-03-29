from app.api.schemas.levels import CreateLevel, UpdateLevel


class LevelController:
    def __init__(
        self,
    ):
        pass

    async def get_all_levels(
        self,
    ):
        pass

    async def get_level(self, level_id: int):
        pass

    async def create_level(self, level: CreateLevel):
        pass

    async def update_level(self, level: UpdateLevel, level_id: int):
        pass

    async def delete_level(self, level_id: int):
        pass
