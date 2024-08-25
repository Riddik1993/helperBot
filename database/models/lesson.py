from datetime import datetime
from sqlalchemy import DateTime, Text, func, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import Base


class Lesson(Base):
    """Модель урока, содержащая предмет урока,
    его дату и время"""

    __tablename__ = "lessons"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(Integer)
    subject: Mapped[str] = mapped_column(Text, nullable=False)
    lesson_dttm: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
