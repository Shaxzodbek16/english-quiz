from sqlalchemy import Column, ForeignKey, Text, Enum, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.api.utils.enums import TestTypeEnum
from app.core.models.base import Base


class Test(Base):
    __tablename__ = "tests"

    level_id = Column(Integer, ForeignKey("levels.id"), nullable=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    question = Column(Text, nullable=False)
    image = Column(String(255), nullable=True)
    type: Mapped[TestTypeEnum] = mapped_column(
        Enum(TestTypeEnum, name="testtypeenum"), nullable=False
    )
    level = relationship("Level", back_populates="tests", cascade="all, delete")
    topic = relationship("Topic", back_populates="tests", cascade="all, delete")
    options = relationship("Option", back_populates="test", cascade="all, delete")
    user_tests = relationship("UserTest", back_populates="test", cascade="all, delete")

    def __repr__(self):
        return f"<Test {self.question}>"

    def to_dict(self):
        return {
            "level_id": self.level_id,
            "topic_id": self.topic_id,
            "question": self.question,
            "type": self.type,
        }
