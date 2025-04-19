from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.core.models.base import Base

if TYPE_CHECKING:
    from app.api.models import Test, UserStatistic


class Topic(Base):
    __tablename__ = "topics"

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    image: Mapped[None | str] = mapped_column(String(255), nullable=True)

    tests: Mapped[list["Test"]] = relationship(
        "Test", back_populates="topic", cascade="all, delete"
    )
    user_statistics: Mapped[list["UserStatistic"]] = relationship(
        "UserStatistic", back_populates="topic", cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"<Topic {self.name}>"

    def to_dict(self) -> dict:
        return {"name": self.name, "image": self.image}
