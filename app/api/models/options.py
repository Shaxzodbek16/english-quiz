from sqlalchemy import Column, ForeignKey, Boolean, Text, Integer
from sqlalchemy.orm import relationship

from app.core.models.base import Base


class Option(Base):
    __tablename__ = "options"

    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    option_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)

    test = relationship("Test", back_populates="options")

    def __repr__(self):
        return f"<Option {self.option_text}>"

    def to_dict(self):
        return {
            "option_text": self.option_text,
            "is_correct": self.is_correct
        }
