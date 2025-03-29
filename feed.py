import asyncio
import random
from datetime import datetime

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import create_engine

from app.api.utils.enums import TestTypeEnum
from app.core.databases.postgres import get_general_session
from app.api.models.users import User
from app.api.models.levels import Level
from app.api.models.topics import Topic
from app.api.models.tests import Test
from app.api.models.user_statistics import UserStatistic
from app.api.models.options import Option
from app.api.models.user_tests import UserTest
from app.api.models.admins import AdminUsers
from app.core.models.base import Base
from app.core.settings import Settings, get_settings

settings: Settings = get_settings()

engine = create_engine("postgresql+psycopg2://" + settings.get_postgres_url)


class Feed:
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session
        self.__faker = Faker()

    async def __drop_all_tables(self) -> None:  # noqa
        Base.metadata.drop_all(bind=engine)
        await asyncio.sleep(3)
        Base.metadata.create_all(bind=engine)
        await asyncio.sleep(3)

    async def _feed_admin_model(self, count: int) -> int:
        for _ in range(count):
            admin_user = AdminUsers(
                first_name=self.__faker.first_name(),
                last_name=self.__faker.last_name(),
                email=self.__faker.email(),
                password=self.__faker.password(),
                is_admin=self.__faker.boolean(chance_of_getting_true=80),
                is_superuser=self.__faker.boolean(chance_of_getting_true=0),
            )
            self.__session.add(admin_user)
        await self.__session.commit()
        return count

    async def _feed_user_model(self, count: int) -> int:
        for _ in range(count):
            user = User(
                first_name=self.__faker.first_name(),
                last_name=self.__faker.last_name(),
                telegram_id=self.__faker.random_int(min=10**10, max=10**12),
                is_active=self.__faker.boolean(chance_of_getting_true=80),
                language=random.choice(["en", "uz", "ru"]),
            )
            self.__session.add(user)
        await self.__session.commit()
        return count

    async def _feed_level_model(self, count: int) -> int:
        for _ in range(count):
            level = Level(
                name=self.__faker.text(max_nb_chars=20),
                image=self.__faker.image_url(),
            )
            self.__session.add(level)
        await self.__session.commit()
        return count

    async def _feed_topic_model(self, count: int) -> int:
        for _ in range(count):
            topic = Topic(
                name=self.__faker.text(max_nb_chars=20),
                image=self.__faker.image_url(),
            )
            self.__session.add(topic)
        await self.__session.commit()
        return count

    async def _feed_test_model(
        self, *, count: int, level_id: int, topic_id: int
    ) -> int:
        for _ in range(count):
            test = Test(
                level_id=self.__faker.random_int(min=1, max=level_id),
                topic_id=self.__faker.random_int(min=1, max=topic_id),
                question=self.__faker.sentence(),
                image=self.__faker.image_url(),
                type=random.choice(
                    [TestTypeEnum.MULTIPLE_CHOICE, TestTypeEnum.GAP_FILLING]
                ),
            )
            self.__session.add(test)
        await self.__session.commit()
        return count

    async def _feed_user_statistics_model(
        self, *, count: int, user_id: int, level_id: int, topic_id: int
    ) -> int:
        for _ in range(count):
            user_statistics = UserStatistic(
                user_id=self.__faker.random_int(min=1, max=user_id),
                level_id=self.__faker.random_int(min=1, max=level_id),
                topic_id=self.__faker.random_int(min=1, max=topic_id),
                total_tests=self.__faker.random_int(min=0, max=100),
                correct_answers=self.__faker.random_int(min=0, max=30),
                total_time_spent_minutes=self.__faker.random_int(min=0, max=1000),
            )
            self.__session.add(user_statistics)
        await self.__session.commit()
        return count

    async def _feed_option_model(self, *, count: int, test_id: int) -> int:
        for _ in range(count):
            option = Option(
                test_id=self.__faker.random_int(min=1, max=test_id),
                option_text=self.__faker.sentence(),
                is_correct=self.__faker.boolean(chance_of_getting_true=33),
            )
            self.__session.add(option)
        await self.__session.commit()
        return count

    async def _feed_user_tests_model(
        self, *, count: int, user_id: int, test_id: int, option_id: int
    ) -> int:
        for _ in range(count):
            user_test = UserTest(
                user_id=self.__faker.random_int(min=1, max=user_id),
                test_id=self.__faker.random_int(min=1, max=test_id),
                selected_option_id=self.__faker.random_int(min=1, max=option_id),
                is_correct=self.__faker.boolean(chance_of_getting_true=33),
                created_at=self.__faker.date_time(end_datetime=datetime.today()),
            )
            self.__session.add(user_test)
        await self.__session.commit()
        return count

    async def run(self):
        await self.__drop_all_tables()
        max_users = await self._feed_user_model(100)
        max_levels = await self._feed_level_model(20)
        max_topics = await self._feed_topic_model(20)
        max_tests = await self._feed_test_model(
            count=100, level_id=max_levels, topic_id=max_topics
        )
        max_options = await self._feed_option_model(count=100, test_id=max_tests)
        await self._feed_user_tests_model(
            count=100, user_id=max_users, test_id=max_tests, option_id=max_options
        )
        await self._feed_user_statistics_model(
            count=30, user_id=max_users, level_id=max_levels, topic_id=max_topics
        )
        print("\nSuccessfully fed the data to the models\n")


async def main():
    async for session in get_general_session():
        feed = Feed(session)
        await feed.run()


if __name__ == "__main__":
    asyncio.run(main())
