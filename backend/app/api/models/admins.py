from sqlalchemy import String, BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.core.models.base import Base


class AdminUsers(Base):
    __tablename__ = "admins"

    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(
        String(255), nullable=False, index=True, unique=True
    )
    telegram_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, nullable=False, index=True
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "telegram_id": self.telegram_id,
            "is_admin": self.is_admin,
            "is_superuser": self.is_superuser,
        }

    def __repr__(self) -> str:
        return f"<AdminUser {self.first_name} {self.last_name}>"

    def __str__(self) -> str:
        return self.__repr__()

    def get_id(self) -> int:
        return self.id
