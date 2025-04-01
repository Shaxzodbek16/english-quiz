from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.core.models.base import Base


class Topic(Base):
    __tablename__ = "topics"

    name = Column(String(255), unique=True, nullable=False)
    image = Column(String(255), nullable=True)

    tests = relationship("Test", back_populates="topic", cascade="all, delete")
    user_statistics = relationship(
        "UserStatistic", back_populates="topic", cascade="all, delete"
    )

    def __repr__(self):
        return f"<Topic {self.name}>"

    def to_dict(self):
        return {"name": self.name, "image": self.image}
