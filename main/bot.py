import telebot
from telebot import types
from os import getenv
from dotenv import load_dotenv

# Database
from database_control import FDataBase, connect_db


def main():

    load_dotenv()  # Load environment variables from .env file
    bot_token = getenv("BOT_TOKEN")  # Get the bot token from an environment variable
    bot = telebot.TeleBot(bot_token)

    @bot.message_handler(commands=['start'])
    def start(message):
        markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup_2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        btn1 = types.KeyboardButton("❓ Help")
        btn2 = types.KeyboardButton("📎 Link to GitHub")
        btn3 = types.KeyboardButton("💻 My Telegram link")
        btn4 = types.KeyboardButton("🤡 I want to registration")
        btn5 = types.KeyboardButton("🔐 Get my token")
        btn6 = types.KeyboardButton("📖 View table")
        btn7 = types.KeyboardButton("📈 Add income")
        btn8 = types.KeyboardButton("📉 Add expense")

        markup_1.add(btn1, btn2, btn5, btn6, btn7, btn8)
        markup_2.add(btn1, btn2, btn3, btn4)

        # check user in our project
        bot_db = FDataBase(connect_db())
        res: bool | str = bot_db.get_username_by_tg_link("https://t.me/" + message.from_user.username)

        if res:
            bot_db.update_user_last_login(res)
            bot.send_message(message.chat.id, f"Hello, {res}!\n"
                                              f"We recognized you. Welcome!", reply_markup=markup_1)
        else:
            bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name} {message.from_user.last_name}!\n"
                                              f"We didn't recognize you. Would you like to register in the project?",
                             reply_markup=markup_2)

    @bot.message_handler(commands=['help'])
    def help(message):
        bot.send_message(message.chat.id, f"{message}")

    @bot.message_handler(commands=['my_link'])
    def my_link(message):
        bot.send_message(message.chat.id, f"Link to your telegram: https://t.me/{message.from_user.username}")

    @bot.message_handler(commands=['project_github'])
    def project_github(message):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("github.com", url="https://github.com/MothScientist/budget_control"))
        bot.send_message(message.chat.id, "Our open-source project on Github:", reply_markup=markup)

    @bot.message_handler(commands=['get_token'])
    def get_token(message):
        bot_db = FDataBase(connect_db())
        token = bot_db.get_token_by_telegram_link("https://t.me/" + message.from_user.username)
        bot.send_message(message.chat.id, f"Your group token:\n{token}")

    @bot.message_handler(content_types=['text'])
    def text(message):
        if message.text == "❓ Help":
            help(message)

        elif message.text == "📎 Link to GitHub":
            project_github(message)

        elif message.text == "💻 My Telegram link":
            my_link(message)

        elif message.text == "🤡 I want to register":
            pass

        elif message.text == "🔐 Get my token":
            get_token(message)

        elif message.text == "📖 View table":
            pass

        elif message.text == "📈 Add income":
            pass

        elif message.text == "📉 Add expense":
            pass

    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
