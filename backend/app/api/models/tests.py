from sqlalchemy import ForeignKey, Text, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from datetime import datetime, UTC

from app.core.models.base import Base

if TYPE_CHECKING:
    from app.api.models.levels import Level
    from app.api.models.topics import Topic
    from app.api.models.test_types import TestTypes
    from app.api.models.user_tests import UserTest


class Test(Base):
    __tablename__ = "tests"

    level_id: Mapped[int] = mapped_column(ForeignKey("levels.id"))
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"))
    type_id: Mapped[int] = mapped_column(ForeignKey("test_types.id"))

    question: Mapped[str] = mapped_column(Text, nullable=False)
    image: Mapped[str | None] = mapped_column(String(255), nullable=True)
    answer_explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    option_ids: Mapped[list[int]] = mapped_column(JSON, default=list)

    level: Mapped["Level"] = relationship(back_populates="tests", cascade="all, delete")
    topic: Mapped["Topic"] = relationship(back_populates="tests", cascade="all, delete")
    type: Mapped["TestTypes"] = relationship(
        back_populates="tests", cascade="all, delete"
    )
    user_tests: Mapped[list["UserTest"]] = relationship(
        back_populates="test", cascade="all, delete"
    )

    def __repr__(self):
        return f"<Test {self.question}>"

    def __str__(self):
        return self.question

    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question,
            "image": self.image,
            "answer_explanation": self.answer_explanation,
            "option_ids": self.option_ids,
            "level_id": self.level_id,
            "topic_id": self.topic_id,
            "type_id": self.type_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def update(self, data: dict[str, str]):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        setattr(self, "created_at", datetime.now(UTC))
        return self

    def __eq__(self, other):
        if isinstance(other, Test):
            return self.question == other.question
        return False
