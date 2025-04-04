from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.core.models.base import Base


class UserStatistic(Base):
    __tablename__ = "user_statistics"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    total_tests = Column(Integer, default=0)
    correct_answers = Column(Integer, default=0)
    total_time_spent_minutes = Column(Integer, default=0)

    user = relationship("User", back_populates="user_statistics", cascade="all, delete")
    level = relationship(
        "Level", back_populates="user_statistics", cascade="all, delete"
    )
    topic = relationship(
        "Topic", back_populates="user_statistics", cascade="all, delete"
    )

    def __repr__(self):
        return f"<UserStatistic {self.user_id} - {self.level_id} - {self.topic_id}>"

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "level_id": self.level_id,
            "topic_id": self.topic_id,
            "total_tests": self.total_tests,
            "correct_answers": self.correct_answers,
            "total_time_spent_minutes": self.total_time_spent_minutes,
        }
