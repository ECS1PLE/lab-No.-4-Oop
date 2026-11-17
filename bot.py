import os

import telebot
from show_commands import ShowCommands
from dotenv import load_dotenv

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

def run_bot():
    bot.infinity_polling()
    print("Бот запущен. Ожидание сообщений...")
