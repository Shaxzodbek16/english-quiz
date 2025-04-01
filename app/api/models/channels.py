from sqlalchemy import Column, String, BigInteger

from app.core.models.base import Base


class Channel(Base):
    __tablename__ = "channels"
    name = Column(String, nullable=False)
    link = Column(String, nullable=False)
    channel_id = Column(BigInteger, unique=True)

    def __repr__(self):
        return f"<Channel(name={self.name}, link={self.link}, channel_id={self.channel_id})>"

    def __str__(self):
        return (
            f"Channel(name={self.name}, link={self.link}, channel_id={self.channel_id})"
        )

    def to_dict(self):
        return {
            "name": self.name,
            "link": self.link,
            "channel_id": self.channel_id,
        }

    def __eq__(self, other):
        if isinstance(other, Channel):
            return False
        return self.channel_id == other.channel_id
