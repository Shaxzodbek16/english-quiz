from datetime import datetime, UTC

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.core.models.base import Base


class Level(Base):
    __tablename__ = "levels"

    name = Column(String(50), unique=True, nullable=False)
    image = Column(String(255), nullable=True)

    tests = relationship("Test", back_populates="level", cascade="all, delete")
    user_statistics = relationship(
        "UserStatistic", back_populates="level", cascade="all, delete"
    )

    def to_dict(self):
        return {
            "name": self.name,
            "image": self.image,
        }

    def update(self, level: dict[str, str | None]) -> "Level":
        for key, value in level.items():
            if hasattr(self, key):
                setattr(self, key, value)
        setattr(self, "updated_at", datetime.now(UTC))
        return self

    def __repr__(self):
        return f"<Level {self.name}>"

    def __str__(self):
        return str(self.name).lower().strip()
