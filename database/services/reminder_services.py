from sqlalchemy import select, cast
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.reminder import Reminder

from lexicon.lexicon import LEXICON_RU


async def save_reminder(session: AsyncSession, text: str):
    stmt = insert(Reminder).values({"text": text})
    await session.execute(stmt)
    await session.commit()


async def get_last_reminder(session: AsyncSession) -> str:
    current_reminder = await __get_last_reminder_from_db(session)
    if current_reminder is not None:
        return current_reminder.text
    else:
        return LEXICON_RU["reminder_not_set"]


async def __get_last_reminder_from_db(session: AsyncSession):
    stmt = select(Reminder).order_by(Reminder.created_at.desc())
    result = await session.execute(stmt)
    await session.commit()
    if result.scalars() is not None:
        return result.scalars().first()
