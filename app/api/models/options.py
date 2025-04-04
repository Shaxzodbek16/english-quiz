from sqlalchemy import Column, Boolean, Text
from datetime import datetime, UTC
from app.core.models.base import Base


class Option(Base):
    __tablename__ = "options"

    option = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Option {self.option}>"

    def to_dict(self):
        return {
            "id": self.id,
            "option_text": self.option,
            "is_correct": self.is_correct,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def update(self, data: dict) -> "Option":
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        setattr(self, "updated_at", datetime.now(UTC))
        return self
