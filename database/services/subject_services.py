from sqlalchemy import select, cast, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from database.models.subject import Subject


async def save_new_subject(session: AsyncSession, subject_name: str):
    stmt = insert(Subject).values({"name": subject_name})
    await session.execute(stmt)
    await session.commit()


async def delete_subject(session: AsyncSession, subject_id: int):
    stmt = delete(Subject).where(Subject.id == subject_id)
    await session.execute(stmt)
    await session.commit()

async def get_all_subjects(session: AsyncSession) -> list[Subject]:
    stmt = select(Subject)
    result = await session.execute(stmt)
    return result.scalars().all()
