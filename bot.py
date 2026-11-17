import os

import telebot
from dotenv import load_dotenv

from show_commands import ShowCommands
from bot_getter import DayCommand

load_dotenv()

bot = telebot.TeleBot(os.environ["BOT_TOKEN"])


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Привет! Я бот расписания ЛЭТИ. Создан студентами группы 5353 Вавиловым Артёмом и Филиппенковым Александром."
    "\nВведите /help, чтобы увидеть список доступных команд.")

@bot.message_handler(commands=["help"])
def help_command(message):
    commands_list = ShowCommands.show_commands()
    bot.reply_to(message, commands_list)

@bot.message_handler(commands=["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"])
def day_schedule(message):
    try:
        day_command = DayCommand(message.text)
        day_index, week_number, group_number = day_command.parse()
        schedule = DayCommand.get_schedule_bot(day_index, week_number, group_number)
        bot.reply_to(message, schedule)
    except ValueError as e:
        bot.reply_to(message, str(e))

@bot.message_handler(commands=["week"])
def week_schedule(message):
    try:
        day_command = DayCommand(message.text)
        _, week_number, group_number = day_command.parse()
        schedule = DayCommand.get_week_schedule_bot(week_number, group_number)
        bot.reply_to(message, schedule)
    except ValueError as e:
        bot.reply_to(message, str(e)) 

def run_bot():
    bot.infinity_polling()
    print("Бот запущен. Ожидание сообщений...")