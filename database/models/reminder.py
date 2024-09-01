from datetime import datetime
from sqlalchemy import BigInteger, DateTime, Text, func, Integer
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import Base


class Reminder(Base):
    __tablename__ = "reminders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
