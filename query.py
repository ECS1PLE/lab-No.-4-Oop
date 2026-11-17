from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

import requests

from const import API_PATH


class ScheduleService:
    def __init__(self, group_number: str, day_index: int | None = None) -> None:
        self.__group_number = group_number
        self.__day_index = day_index

    def get_schedule(self) -> dict:
        group_number = self.__group_number
        response = requests.get(
            API_PATH,
            params={"groupNumber": group_number, "joinWeeks": "false"},
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()
        if group_number not in data:
            raise LookupError(f"Расписание группы {group_number} не найдено")

        return data[group_number]

    def format_schedule(self, schedule: dict) -> str:
        lines = [f"Расписание группы {self.__group_number}:"]

        for day in schedule["days"].values():
            lines.append(f"\n{day['name']}:")

            if not day["lessons"]:
                lines.append("Нет занятий")
                continue

            for lesson in day["lessons"]:
                lines.append(
                    f"{lesson['start_time']}-{lesson['end_time']} "
                    f"{lesson['name']} (неделя {lesson['week']})"
                )

        return "\n".join(lines)

    def print_schedule(self, schedule: dict) -> None:
        print(self.format_schedule(schedule))

    def get_day_schedule(self, week_number: int, day_index: int | None = None) -> dict:
        if day_index is None:
            day_index = self.__day_index

        if day_index is None:
            raise ValueError("Укажите индекс дня недели")

        days = self.get_week_schedule(week_number)["days"]
        day_key = str(day_index)

        if day_key not in days:
            raise ValueError(f"День с индексом {day_index} отсутствует в расписании")

        return days[day_key]

    def get_week_schedule(self, week_number: int) -> dict:
        if week_number not in (1, 2, 3):
            raise ValueError("Введите 1, 2 или 3")

        schedule = self.get_schedule()
        if week_number == 3:
            return schedule

        week = str(week_number)
        for day in schedule["days"].values():
            day["lessons"] = [
                lesson for lesson in day["lessons"]
                if lesson["week"] == week
            ]
        return schedule

    def get_tomorrow_schedule(self, week_number: int) -> dict:
        today = datetime.now(ZoneInfo("Europe/Moscow"))
        tomorrow_index = (today.weekday() + 1) % 7
        return self.get_day_schedule(week_number, tomorrow_index)

    def get_today_schedule(self, week_number: int) -> dict:
        today_index = datetime.now(ZoneInfo("Europe/Moscow")).weekday()
        return self.get_day_schedule(week_number, today_index)

    def get_next_lesson(self, week_number: int) -> tuple[datetime, dict]:
        if week_number not in (1, 2, 3):
            raise ValueError("Введите 1, 2 или 3")

        now = datetime.now(ZoneInfo("Europe/Moscow"))
        days = self.get_schedule()["days"]

        for offset in range(15):
            date = now.date() + timedelta(days=offset)
            lessons = days.get(str(date.weekday()), {}).get("lessons", [])

            if week_number != 3:
                weeks_passed = (now.weekday() + offset) // 7
                active_week = str((week_number - 1 + weeks_passed) % 2 + 1)
                lessons = [lesson for lesson in lessons if lesson["week"] == active_week]

            next_lesson = None
            for lesson in lessons:
                start_time = time.fromisoformat(lesson["start_time"])
                if offset == 0 and start_time <= now.time():
                    continue

                if next_lesson is None or start_time < next_lesson[0]:
                    next_lesson = start_time, lesson

            if next_lesson is not None:
                start_time, lesson = next_lesson
                return datetime.combine(date, start_time, tzinfo=now.tzinfo), lesson

        raise LookupError("Ближайшая пара не найдена.")

    def get_lesson_info(self, week_number: int, day_index: int, lesson_name: str) -> dict:
        day_schedule = self.get_day_schedule(week_number, day_index)
        lessons = day_schedule["lessons"]

        res = []

        for lesson in lessons:
            if lesson["name"] == lesson_name:
                res.append(lesson)

        if not res:
            raise ValueError(
                f"Занятие '{lesson_name}' не найдено "
                f"в расписании на день с индексом {day_index}"
            )

        return res

    @staticmethod
    def format_lesson_info(lesson_info: dict) -> str:
        return (
            f"Название: {lesson_info['name']}\n"
            f"Тип: {lesson_info['subjectType']}\n"
            f"Время: {lesson_info['start_time']} - {lesson_info['end_time']}\n"
            f"Неделя: {lesson_info['week']}\n"
            f"Аудитория: {lesson_info['room']}\n"
            f"Преподаватель: {lesson_info['teacher']}"
        )
