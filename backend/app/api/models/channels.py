from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from app.core.models.base import Base


class Channel(Base):
    __tablename__ = "channels"

    name: Mapped[str] = mapped_column(String, nullable=False)
    link: Mapped[str] = mapped_column(String, nullable=False)
    channel_id: Mapped[int] = mapped_column(BigInteger, unique=True)

    def __repr__(self) -> str:
        return f"<Channel(name={self.name}, link={self.link}, channel_id={self.channel_id})>"

    def __str__(self) -> str:
        return self.__repr__()

    def to_dict(self) -> dict[str, str | int]:
        return {
            "name": self.name,
            "link": self.link,
            "channel_id": self.channel_id,
        }

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Channel):
            return NotImplemented
        return self.channel_id == other.channel_id
