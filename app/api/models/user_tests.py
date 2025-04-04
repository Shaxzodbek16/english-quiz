from sqlalchemy import Column, ForeignKey, Boolean, TIMESTAMP, func, Integer
from sqlalchemy.orm import relationship

from app.core.models.base import Base


class UserTest(Base):
    __tablename__ = "user_tests"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    test_id = Column(Integer, ForeignKey("tests.id", ondelete="CASCADE"), nullable=True)
    selected_option_id = Column(
        Integer, ForeignKey("options.id", ondelete="SET NULL"), nullable=True
    )
    is_correct = Column(Boolean, nullable=False)

    user = relationship("User", back_populates="user_tests", cascade="all, delete")
    test = relationship("Test", back_populates="user_tests", cascade="all, delete")

    def __repr__(self):
        return f"<UserTest {self.user_id} - {self.test_id}>"

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "test_id": self.test_id,
            "selected_option_id": self.selected_option_id,
            "is_correct": self.is_correct,
        }
