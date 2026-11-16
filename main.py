from query import ScheduleClient

def main() -> None:
    while True:
        group_number = input("Введите номер группы: ").strip()
        if not group_number:
            print("Введите номер группы, например 5353.")
            continue

        client = ScheduleClient(group_number)

        try:
            client.print_schedule()
        except LookupError as error:
            print(error)
            continue

if __name__ == "__main__":
    main()