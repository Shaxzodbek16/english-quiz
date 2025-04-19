from sqlalchemy import BigInteger, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.core.models.base import Base

if TYPE_CHECKING:
    from app.api.models import UserStatistic, UserTest


class User(Base):
    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, nullable=False, index=True
    )
    language: Mapped[str | None] = mapped_column(
        String(10), nullable=True, default="en"
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    user_tests: Mapped[list["UserTest"]] = relationship(
        "UserTest", back_populates="user"
    )
    user_statistics: Mapped[list["UserStatistic"]] = relationship(
        "UserStatistic", back_populates="user"
    )

    @property
    def full_name(self) -> str:
        return (
            self.first_name
            if self.last_name is None
            else f"{self.first_name} {self.last_name}"
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "telegram_id": self.telegram_id,
            "is_active": self.is_active,
            "language": self.language,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __repr__(self) -> str:
        return f"<User {self.first_name} {self.last_name}>"

    def get_id(self) -> int:
        return self.id
