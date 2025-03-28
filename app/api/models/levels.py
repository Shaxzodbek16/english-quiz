from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from app.core.models.base import Base


class Level(Base):
    __tablename__ = "levels"

    name = Column(String(50), unique=True, nullable=False)
    image = Column(String(255), nullable=True)

    tests = relationship("Test", back_populates="level")
    user_statistics = relationship("UserStatistic", back_populates="level")

    def __repr__(self):
        return f"<Level {self.name}>"

    def to_dict(self):
        return {
            "name": self.name
        }