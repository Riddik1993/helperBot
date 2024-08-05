from sqlalchemy import select, cast
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.reminder import Reminder
from database.models.user import User
from lexicon.lexicon import LEXICON_RU


async def upsert_user(
    session: AsyncSession,
    telegram_id: int,
    first_name: str,
    last_name: str | None = None,
):
    """
    Добавление или обновление пользователя
    в таблице users
    :param session: сессия СУБД
    :param telegram_id: айди пользователя
    :param first_name: имя пользователя
    :param last_name: фамилия пользователя
    """
    stmt = insert(User).values(
        {
            "telegram_id": telegram_id,
            "first_name": first_name,
            "last_name": last_name,
        }
    )
    stmt = stmt.on_conflict_do_update(
        index_elements=["telegram_id"],
        set_=dict(
            first_name=first_name,
            last_name=last_name,
        ),
    )
    await session.execute(stmt)
    await session.commit()


async def save_reminder(session: AsyncSession, text: str):
    stmt = insert(Reminder).values({"text": text})
    await session.execute(stmt)
    await session.commit()


async def get_last_reminder(session: AsyncSession) -> str:
    current_reminder = await __get_last_reminder_from_db(session)
    print(current_reminder)
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
