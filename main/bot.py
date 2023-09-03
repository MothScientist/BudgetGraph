import telebot
from telebot import types
import os
from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env file
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Get the bot token from an environment variable
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    btn1 = types.KeyboardButton("❓ Help")
    btn2 = types.KeyboardButton("🏆 Link to project github")
    btn3 = types.KeyboardButton("💻 My Telegram link")

    markup.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name} {message.from_user.last_name}!\n"
                                      f"Are you a new user or contributor to the project?", reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f"{message.from_user.first_name} {message.from_user.last_name},"
                                      f" Here is a list of commands to help you ->")


@bot.message_handler(commands=['my_link'])
def my_link(message):
    bot.send_message(message.chat.id, f"Link to your telegram: https://t.me/{message.from_user.username}")


@bot.message_handler(commands=['project_github'])
def project_github(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("github.com", url="https://github.com/MothScientist/budget_control"))
    bot.send_message(message.chat.id, "Our open-source project on Github:", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == "❓ Help":
        help(message)

    elif message.text == "🏆 Link to project github":
        project_github(message)

    elif message.text == "💻 My Telegram link":
        my_link(message)


bot.polling(none_stop=True)
