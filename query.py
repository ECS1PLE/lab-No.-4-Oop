import requests

from const import API_PATH


class ScheduleClient:
    def __init__(self, group_number: str = None):
        self.__group_number = group_number

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

    def print_schedule(self) -> None:
        schedule = self.get_schedule()
        print(f"\nРасписание группы {self.__group_number}:")
        for _, day in schedule["days"].items():
            if not day["lessons"]:
                print(f"\n{day['name']}: нет занятий")
                continue
            
            print(f"\n{day['name']}:")
            for lesson in day["lessons"]:
                print(
                    f"{lesson['start_time']}-{lesson['end_time']} "
                    f"{lesson['name']} (неделя {lesson['week']})"
                )

if __name__ == "__main__":
    group_number = input("Введите номер группы: ").strip()
    client = ScheduleClient(group_number)
    client.print_schedule()
