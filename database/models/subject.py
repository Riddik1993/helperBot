from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import Base
from database.models.mixins import TimestampMixin


class Subject(Base, TimestampMixin):
    """Предметы"""
    __tablename__ = "subjects"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text)
