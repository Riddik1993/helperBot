from datetime import datetime
from sqlalchemy import DateTime, Text, func, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base
from database.models.mixins import TimestampMixin


class Lesson(Base, TimestampMixin):
    __tablename__ = "lessons"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    subject = relationship("Subject", back_populates="lessons", lazy="selectin")
    lesson_dttm: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
