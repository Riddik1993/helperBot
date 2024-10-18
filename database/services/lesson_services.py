from sqlalchemy import select, insert
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

async def add_new_lesson(session: AsyncSession, subject_name: str):
    stmt = insert(Lesson).values({"name": subject_name})
    await session.execute(stmt)
    await session.commit()
