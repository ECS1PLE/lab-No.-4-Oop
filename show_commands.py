from const import HELP_COMMANDS


class CommandHelp:
    @staticmethod
    def format_text() -> str:
        commands = "\n".join(
            f"{command}: {description}"
            for command, description in HELP_COMMANDS.items()
        )
        return f"Список доступных команд:\n{commands}\n"
