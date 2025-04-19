from datetime import datetime, UTC
from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.models.base import Base

if TYPE_CHECKING:
    from app.api.models import Test


class TestTypes(Base):
    __tablename__ = "test_types"

    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    tests: Mapped[list["Test"]] = relationship(
        "Test", back_populates="type", cascade="all, delete"
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def update(self, data: dict[str, str | None]) -> "TestTypes":
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        setattr(self, "updated_at", datetime.now(UTC))
        return self

    def __repr__(self) -> str:
        return f"<TestType {self.name}>"

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        if isinstance(other, TestTypes):
            return self.name == other.name
        return False
