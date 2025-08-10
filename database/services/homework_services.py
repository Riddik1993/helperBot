from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.homework import Homework
from lexicon.lexicon import LexiconRu
from utils.formatting import make_bold


async def get_last_homework_for_student(session: AsyncSession, student_id: int) -> str:
    student_homework = await __get_last_homework_for_student_from_db(
        session, student_id
    )
    if student_homework is not None:
        homework_dttm = student_homework.created_at.strftime("%d.%m.%Y %H:%M")
        homework_task_text = student_homework.text if student_homework.text else ""
        homework_text = make_bold(f"Задание от {homework_dttm}:\n") + homework_task_text

    else:
        homework_text = LexiconRu.homework_not_found.value
    return homework_text


async def save_homework_for_student(
        session: AsyncSession, student_id: int, homework_text: str
):
    stmt = insert(Homework).values({"student_id": student_id, "text": homework_text})
    await session.execute(stmt)
    await session.commit()


async def __get_last_homework_for_student_from_db(
        session: AsyncSession, student_id: int
) -> Homework | None:
    stmt = (
        select(Homework)
        .where(Homework.student_id == student_id)
        .order_by(Homework.created_at.desc())
    )
    result = await session.execute(stmt)
    return result.scalars().first()
