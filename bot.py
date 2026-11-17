import os

import telebot
from dotenv import load_dotenv

from bot_getter import ScheduleCommand
from show_commands import CommandHelp

load_dotenv()

bot = telebot.TeleBot(os.environ["BOT_TOKEN"])


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "Привет! Я бот расписания ЛЭТИ. Создан студентами группы 5353 "
        "Вавиловым Артёмом и Филиппенковым Александром."
        "\nВведите /help, чтобы увидеть список доступных команд.",
    )


@bot.message_handler(commands=["help"])
def help_command(message):
    commands_list = CommandHelp.format_text()
    bot.reply_to(message, commands_list)


@bot.message_handler(commands=[
    "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
])
def day_schedule(message):
    try:
        command = ScheduleCommand(message.text)
        day_index, week_number, group_number = command.parse()
        schedule = ScheduleCommand.get_day_schedule(day_index, week_number, group_number)
        bot.reply_to(message, schedule)
    except (ValueError, LookupError) as error:
        bot.reply_to(message, str(error))


@bot.message_handler(commands=["week"])
def week_schedule(message):
    try:
        command = ScheduleCommand(message.text)
        _, week_number, group_number = command.parse()
        schedule = ScheduleCommand.get_week_schedule(week_number, group_number)
        bot.reply_to(message, schedule)
    except (ValueError, LookupError) as error:
        bot.reply_to(message, str(error))


@bot.message_handler(commands=["tomorrow"])
def tomorrow_schedule(message):
    try:
        command = ScheduleCommand(message.text)
        _, week_number, group_number = command.parse()
        schedule = ScheduleCommand.get_tomorrow_schedule(week_number, group_number)
        bot.reply_to(message, schedule)
    except (ValueError, LookupError) as error:
        bot.reply_to(message, str(error))


@bot.message_handler(commands=["today"])
def today_schedule(message):
    try:
        command = ScheduleCommand(message.text)
        _, week_number, group_number = command.parse()
        schedule = ScheduleCommand.get_today_schedule(week_number, group_number)
        bot.reply_to(message, schedule)
    except (ValueError, LookupError) as error:
        bot.reply_to(message, str(error))


@bot.message_handler(commands=["lesson"])
def lesson_info(message):
    try:
        command = ScheduleCommand(message.text)
        day_index, week_number, group_number, lesson_name = command.parse_lesson()
        lesson = ScheduleCommand.get_lesson_info(
            day_index, week_number, group_number, lesson_name
        )
        bot.reply_to(message, lesson)
    except (ValueError, LookupError) as error:
        bot.reply_to(message, str(error))


def run_bot() -> None:
    print("Бот запущен. Ожидание сообщений...")
    bot.infinity_polling()
