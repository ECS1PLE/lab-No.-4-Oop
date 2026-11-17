from const import HELP_COMMANDS

class ShowCommands:
    @staticmethod
    def show_commands() -> str:
        str = 'Список доступных команд:\n'
        for command, description in HELP_COMMANDS.items():
            str += f"{command}: {description}\n"
        return str