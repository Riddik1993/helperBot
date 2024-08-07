from sqlalchemy import select, cast

from database.models.user import User
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession


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


async def get_all_users(
        session: AsyncSession
) -> list[User]:
    stmt = select(User)
    result = await session.execute(stmt)
    return [student for student in result.scalars()]


async def get_full_user_name_by_id(session: AsyncSession, user_id: int) -> str:
    stmt = select(User).where(User.telegram_id == user_id)
    result = await session.execute(stmt)
    user: User = result.scalar()
    return user.first_name + ' ' + user.last_name
