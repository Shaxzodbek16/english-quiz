from app.core.models.base import Base
from sqlalchemy import Column, String, BigInteger, Boolean


class AdminUsers(Base):
    __tablename__ = "admins"

    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=False, index=True, unique=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)

    is_admin = Column(Boolean, nullable=False, default=False)
    is_superuser = Column(Boolean, nullable=False, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "telegram_id": self.telegram_id,
            "is_admin": self.is_admin,
            "is_superuser": self.is_superuser,
        }

    def __repr__(self):
        return f"<AdminUser {self.first_name} {self.last_name}>"

    def __str__(self):
        return f"<AdminUser {self.first_name} {self.last_name}>"
