from typing import Optional

from aiogram.types import Document
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.homework import Homework
from lexicon.lexicon import LexiconRu
from utils.formatting import make_bold


def prepare_homework_msg_text(homework: Optional[Homework]) -> str:
    if homework:
        homework_dttm = homework.created_at.strftime("%d.%m.%Y %H:%M")
        homework_task_text = (
            homework.text if homework.text else LexiconRu.homework_withoout_text.value
        )

        return make_bold(f"Задание от {homework_dttm}:\n") + homework_task_text
    else:
        return LexiconRu.homework_not_found.value


async def save_homework_for_student(
    session: AsyncSession,
    student_id: int,
    homework_text: Optional[str],
    document: Optional[Document] = None,
):
    student_homework = Homework(
        student_id=student_id,
        text=homework_text,
        files=[document.file_id] if document else [],
    )
    session.add(student_homework)
    await session.commit()


async def get_last_homework_for_student_from_db(
    session: AsyncSession, student_id: int
) -> Homework | None:
    stmt = (
        select(Homework)
        .where(Homework.student_id == student_id)
        .order_by(Homework.created_at.desc())
    )
    result = await session.execute(stmt)
    return result.scalars().first()
