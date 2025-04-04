from sqlalchemy import Column, ForeignKey, Text, Integer, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from app.core.models.base import Base


class Test(Base):
    __tablename__ = "tests"

    level_id = Column(Integer, ForeignKey("levels.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    type_id = Column(Integer, ForeignKey("test_types.id"))

    question = Column(Text, nullable=False)
    image = Column(String(255), nullable=True)
    answer_explanation = Column(Text, nullable=True)
    option_ids = Column(JSON, default=[])

    level = relationship("Level", back_populates="tests", cascade="all, delete")
    topic = relationship("Topic", back_populates="tests", cascade="all, delete")
    type = relationship("TestTypes", back_populates="tests", cascade="all, delete")
    user_tests = relationship("UserTest", back_populates="test", cascade="all, delete")

    def __repr__(self):
        return f"<Test {self.question}>"

    def __str__(self):
        return self.question

    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question,
            "image": self.image,
            "topic_id": self.topic_id,
            "level_id": self.level_id,
            "type_id": self.type_id,
            "answer_hint": self.answer_explanation,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "option_ids": self.option_ids,
        }

    def update(self, data: dict[str, str]):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def __eq__(self, other):
        if isinstance(other, Test):
            return self.question == other.question
        return False
