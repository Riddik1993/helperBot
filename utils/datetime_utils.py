from datetime import datetime


def create_datetime_from_parts(date: str, time: str) -> datetime:
    lesson_dttm_str = date + " " + time
    return datetime.strptime(lesson_dttm_str, "%d.%m.%Y %H:%M")
