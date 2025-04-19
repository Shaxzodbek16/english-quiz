from sqlalchemy import ForeignKey, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.api.models import User, Test

from app.core.models.base import Base


class UserTest(Base):
    __tablename__ = "user_tests"

    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True
    )
    test_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("tests.id", ondelete="CASCADE"), nullable=True
    )
    selected_option_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("options.id", ondelete="SET NULL"), nullable=True
    )
    correct_option_id: Mapped[bool] = mapped_column(Boolean, nullable=False)

    user: Mapped["User"] = relationship(
        "User", back_populates="user_tests", cascade="all, delete"
    )
    test: Mapped["Test"] = relationship(
        "Test", back_populates="user_tests", cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"<UserTest {self.user_id} - {self.test_id}>"

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "test_id": self.test_id,
            "selected_option_id": self.selected_option_id,
            "correct_option_id": self.correct_option_id,
        }
