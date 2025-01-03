from datetime import datetime
import re


def create_datetime_from_parts(date: str, time: str) -> datetime:
    moscow_timezone_str = "+0300"
    lesson_dttm_str = date + " " + time + moscow_timezone_str
    return datetime.strptime(lesson_dttm_str, "%d.%m.%Y %H:%M%z")


def check_time_str_format(time: str) -> bool:
    """
    Метод проверяет корректность введенной строки с временем,
    строка должна соотвествовать шаблону HH:MM
    :param time: Введенная строка с временем
    :return: True если строка корректна, False в противном случае
    """
    time_pattern = "^[0-2]+\d:[0-5]\d$"
    return bool(re.match(time_pattern, time))
