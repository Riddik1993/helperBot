from zoneinfo import ZoneInfo

from database.models.lesson import Lesson


def render_lesson_text(lesson: Lesson) -> str:
    lesson_str = lesson.lesson_dttm.astimezone(ZoneInfo('Europe/Moscow')).strftime("%d.%m.%Y %H:%M")
    return f"{lesson_str} - {lesson.subject.name}"


def render_lessons_for_student(lessons: list[Lesson]) -> str:
    lessons_str_lst = [render_lesson_text(lesson) + "\n" for lesson in
                       lessons]
    return '\n'.join(lessons_str_lst)
