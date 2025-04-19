from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.api.models import User, Topic, Level

from app.core.models.base import Base


class UserStatistic(Base):
    __tablename__ = "user_statistics"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    level_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("levels.id"), nullable=True
    )
    topic_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("topics.id"), nullable=True
    )
    total_tests: Mapped[int] = mapped_column(Integer, default=0)
    correct_answers: Mapped[int] = mapped_column(Integer, default=0)
    total_time_spent_minutes: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["User"] = relationship(
        "User", back_populates="user_statistics", cascade="all, delete"
    )
    level: Mapped["Level"] = relationship(
        "Level", back_populates="user_statistics", cascade="all, delete"
    )
    topic: Mapped["Topic"] = relationship(
        "Topic", back_populates="user_statistics", cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"<UserStatistic {self.user_id} - {self.level_id} - {self.topic_id}>"

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "level_id": self.level_id,
            "topic_id": self.topic_id,
            "total_tests": self.total_tests,
            "correct_answers": self.correct_answers,
            "total_time_spent_minutes": self.total_time_spent_minutes,
        }
