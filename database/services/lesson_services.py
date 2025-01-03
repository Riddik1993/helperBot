from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.lesson import Lesson
from database.models.subject import Subject


async def get_all_lessons_by_user(
        session: AsyncSession, student_id: int
) -> list[Lesson]:
    stmt = (
        select(Lesson)
        .where(Lesson.student_id == student_id)
        .join(Subject)
        .order_by(Lesson.created_at.desc())
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_actual_lessons_by_user(
        session: AsyncSession, student_id: int
) -> list[Lesson]:
    stmt = (
        select(Lesson)
        .where(Lesson.student_id == student_id)
        .where(Lesson.lesson_dttm >= datetime.now(ZoneInfo('Europe/Paris')).date())
        .join(Subject)
        .order_by(Lesson.created_at.desc())
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def add_new_lesson(session: AsyncSession, lesson: Lesson):
    session.add(lesson)
    await session.commit()


async def delete_lesson_by_id(session: AsyncSession, lesson_id: int):
    stmt = delete(Lesson).where(Lesson.id == lesson_id)
    await session.execute(stmt)
    await session.commit()
