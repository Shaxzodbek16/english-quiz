from datetime import datetime, UTC

from sqlalchemy import Column, Text, String
from sqlalchemy.orm import relationship

from app.core.models.base import Base


class TestTypes(Base):
    __tablename__ = "test_types"

    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    tests = relationship("Test", back_populates="type", cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def update(self, data: dict) -> "TestTypes":
        for k, v in data.items():
            if hasattr(self, k):
                setattr(self, k, v)
        setattr(self, "updated_at", datetime.now(UTC))
        return self

    def __repr__(self):
        return f"<TestType {self.name}>"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, TestTypes):
            return self.name == other.name
        return False
