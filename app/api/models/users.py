from sqlalchemy import Column, String, BigInteger, Boolean
from sqlalchemy.orm import relationship

from app.core.models.base import Base


class User(Base):
    __tablename__ = "users"

    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    language = Column(String(10), nullable=True, default="en")
    is_active = Column(Boolean, nullable=False, default=True)

    user_tests = relationship("UserTest", back_populates="user")
    user_statistics = relationship("UserStatistic", back_populates="user")

    @property
    def full_name(self):
        return (
            self.first_name
            if self.last_name is None
            else f"{self.first_name} {self.last_name}"
        )

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "telegram_id": self.telegram_id,
            "is_active": self.is_active,
            "language": self.language,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}>"
