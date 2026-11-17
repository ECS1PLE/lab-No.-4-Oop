from const import day_mapping
from query import ScheduleClient

class DayCommand:
    def __init__(self, command: str) -> None:
        self.__command = command

    def parse(self) -> tuple[int, int, str]:
        parts = self.__command.split(" ")
        if len(parts) != 3:
            raise ValueError("Пример команды: /monday 1 5353")

        command_name = parts[0].lower()
        week = parts[1]
        group_number = parts[2]

        day_index = day_mapping.get(command_name)
        if day_index is None:
            raise ValueError("День недели не распознан. Используй /help.")

        if week not in ("1", "2", "3"):
            raise ValueError("Укажи 1, 2 или 3 для обеих недель.")

        if len(group_number) != 4 or not group_number.isdigit():
            raise ValueError("Номер группы должен состоять из четырёх цифр.")

        return day_index, int(week), group_number

    @staticmethod
    def get_schedule_bot(day_index: int, week_number: int, group_number: str) -> str:
        client = ScheduleClient(group_number, day_index)
        day_schedule = client.get_day_schedule(week_number)
        schedule = {"days": {str(day_index): day_schedule}}
        return client.format_schedule(schedule)

    