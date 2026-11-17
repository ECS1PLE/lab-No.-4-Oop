from const import DAY_COMMANDS, DAY_NAMES, HELP_COMMANDS
from query import ScheduleService


class ScheduleCommand:
    def __init__(self, command: str) -> None:
        self.__command = command

    def parse(self) -> tuple[int | None, int, str]:
        parts = self.__command.split()
        if len(parts) != 3:
            raise ValueError("Пример команды: /monday 1 5353")

        command_name = parts[0].lower()
        day_index = DAY_COMMANDS.get(command_name)

        if day_index is None and command_name not in HELP_COMMANDS:
            raise ValueError("Команда не распознана. Используй /help.")

        week_number, group_number = self._validate_arguments(parts[1], parts[2])
        return day_index, week_number, group_number

    @staticmethod
    def get_day_schedule(day_index: int, week_number: int, group_number: str) -> str:
        client = ScheduleService(group_number, day_index)
        day_schedule = client.get_day_schedule(week_number)
        schedule = {"days": {str(day_index): day_schedule}}
        return client.format_schedule(schedule)

    @staticmethod
    def get_week_schedule(week_number: int, group_number: str) -> str:
        client = ScheduleService(group_number)
        week_schedule = client.get_week_schedule(week_number)
        return client.format_schedule(week_schedule)

    @staticmethod
    def get_tomorrow_schedule(week_number: int, group_number: str) -> str:
        client = ScheduleService(group_number)
        day = client.get_tomorrow_schedule(week_number)
        schedule = {"days": {"tomorrow": day}}
        return client.format_schedule(schedule)

    @staticmethod
    def get_today_schedule(week_number: int, group_number: str) -> str:
        client = ScheduleService(group_number)
        day = client.get_today_schedule(week_number)
        schedule = {"days": {"today": day}}
        return client.format_schedule(schedule)

    @staticmethod
    def get_lesson_info(
        day_index: int, week_number: int, group_number: str, lesson_name: str
    ) -> str:
        client = ScheduleService(group_number)
        lessons = client.get_lesson_info(week_number, day_index, lesson_name)
        return "\n\n".join(client.format_lesson_info(lesson) for lesson in lessons)

    def parse_lesson(self) -> tuple[int, int, str, str]:
        parts = self.__command.split(maxsplit=4)
        if len(parts) != 5:
            raise ValueError(
                "Пример команды: /lesson 2 5353 понедельник Высшая математика"
            )

        _, week, group_number, day_name, lesson_name = parts

        week_number, group_number = self._validate_arguments(week, group_number)

        day_index = DAY_NAMES.get(day_name.capitalize())
        if day_index is None:
            raise ValueError("Укажи день недели по-русски, например понедельник.")

        return day_index, week_number, group_number, lesson_name.strip()

    @staticmethod
    def _validate_arguments(week: str, group_number: str) -> tuple[int, str]:
        if week not in ("1", "2", "3"):
            raise ValueError("Укажи 1, 2 или 3 для обеих недель.")

        if len(group_number) != 4 or not group_number.isdigit():
            raise ValueError("Номер группы должен состоять из четырёх цифр.")

        return int(week), group_number
