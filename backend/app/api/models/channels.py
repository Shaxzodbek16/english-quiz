from typing import Any
from datetime import datetime, UTC
from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models.base import Base


class Channel(Base):
    __tablename__ = "channels"

    name: Mapped[str] = mapped_column(String, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False)
    channel_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    must_subscribe: Mapped[bool] = mapped_column(default=False)

    def update(self, data: dict[str, Any]) -> "Channel":
        for key, value in data.items():
            if hasattr(self, key):
                if value is not None:
                    setattr(self, key, value)
        setattr(self, "updated_at", datetime.now(UTC))
        return self

    def to_dict(self) -> dict[str, str | int]:
        return {
            "name": self.name,
            "link": self.link,
            "channel_id": self.channel_id,
            "must_subscribe": self.must_subscribe,
        }

    def __repr__(self) -> str:
        return f"<Channel(name={self.name}, link={self.link}, channel_id={self.channel_id})>"

    def __str__(self) -> str:
        return self.__repr__()
