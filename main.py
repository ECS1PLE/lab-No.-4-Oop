import argparse

from cli import ScheduleConsole
from bot import run_bot


def run_cli() -> None:
    while True:
        group_number = input("Введите номер группы: ").strip()
        if not group_number:
            print("Введите номер группы, например 5353.")
            continue

        ScheduleConsole(group_number).run()


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--cli", action="store_true")
    mode.add_argument("--bot", action="store_true")
    args = parser.parse_args()

    match args:
        case argparse.Namespace(cli=True, bot=False):
            run_cli()
        case argparse.Namespace(cli=False, bot=True):
            run_bot()
        case _:
            print("Выберите режим работы: --cli или --bot")


if __name__ == "__main__":
    main()
