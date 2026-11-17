from const import day_names
from query import ScheduleClient


class ScheduleCLI:
    def __init__(self, group_number: str) -> None:
        self.__group_number = group_number

    def cli_mode(self) -> None:
        week_input = input("Введите неделю (1, 2 или 3 для обеих): ").strip()
        day_input = input("Введите день недели или нажмите Enter для всей недели: ").strip()

        try:
            week_number = int(week_input)

            if day_input:
                day_index = day_names.get(day_input.capitalize())
                if day_index is None:
                    raise ValueError("Введите название дня недели, например понедельник.")

                client = ScheduleClient(self.__group_number, day_index=day_index)
                day = client.get_day_schedule(week_number)
                schedule = {"days": {str(day_index): day}}
            else:
                client = ScheduleClient(self.__group_number)
                schedule = client.get_week_schedule(week_number)

            client.print_schedule(schedule)
        except (ValueError, LookupError) as error:
            print(error)