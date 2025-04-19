from datetime import datetime, UTC
from typing import Any

from sqlalchemy import Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import Base


class Option(Base):
    __tablename__ = "options"

    option: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"<Option {self.option}>"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "option_text": self.option,
            "is_correct": self.is_correct,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def update(self, data: dict[str, Any]) -> "Option":
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        setattr(self, "updated_at", datetime.now(UTC))
        return self
