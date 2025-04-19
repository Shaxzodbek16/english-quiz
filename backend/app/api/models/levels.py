from datetime import datetime, UTC
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base

if TYPE_CHECKING:
    from app.api.models import Test, UserStatistic


class Level(Base):
    __tablename__ = "levels"

    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    image: Mapped[str | None] = mapped_column(String(255), nullable=True)

    tests: Mapped[list["Test"]] = relationship(
        back_populates="level", cascade="all, delete"
    )
    user_statistics: Mapped[list["UserStatistic"]] = relationship(
        back_populates="level", cascade="all, delete"
    )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "image": self.image,
        }

    def update(self, level: dict[str, str | None]) -> "Level":
        for key, value in level.items():
            if hasattr(self, key):
                setattr(self, key, value)
        setattr(self, "updated_at", datetime.now(UTC))
        return self

    def __repr__(self) -> str:
        return f"<Level {self.name}>"

    def __str__(self) -> str:
        return str(self.name).lower().strip()
