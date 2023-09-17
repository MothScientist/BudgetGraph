import telebot
from telebot import types
from os import getenv
from dotenv import load_dotenv
from password_hashing import getting_hash, get_salt
import re

# Database
from database_control import FDataBase, connect_db, close_db_bot, create_table_group

# Validators
from validators.input_number import input_number
from validators.registration import token_validator


def main():

    load_dotenv()  # Load environment variables from .env file
    bot_token = getenv("BOT_TOKEN")  # Get the bot token from an environment variable
    bot = telebot.TeleBot(bot_token)

    @bot.message_handler(commands=['start'])
    def start(message) -> None:
        # Buttons
        markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup_2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        btn1 = types.KeyboardButton("❓ Help")
        btn2 = types.KeyboardButton("📎 Link to GitHub")
        btn3 = types.KeyboardButton("💻 My Telegram link")
        btn4 = types.KeyboardButton("🤡 I want to register")
        btn5 = types.KeyboardButton("🔐 Get my token")
        btn6 = types.KeyboardButton("📖 View table")
        btn7 = types.KeyboardButton("📈 Add income")
        btn8 = types.KeyboardButton("📉 Add expense")

        markup_1.add(btn1, btn2, btn5, btn6, btn7, btn8)
        markup_2.add(btn1, btn2, btn3, btn4)

        # check user in our project
        connection = connect_db()
        bot_db = FDataBase(connection)
        res: bool | str = bot_db.get_username_by_tg_link("https://t.me/" + message.from_user.username)

        if res:
            bot_db.update_user_last_login(res)
            close_db_bot(connection)

            # to send a sticker from a car in .webp format no larger than 512x512 pixels
            # sticker = open("D:\\telebot\\stickers\\stick_name.webp)", "rb")
            # bot.send_sticker(message.chat.id, sticker)

            bot.send_message(message.chat.id, f"Hello, {res}!\n"
                                              f"We recognized you. Welcome!", reply_markup=markup_1)
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEKUtplB2lgxLm33sr3QSOP0WICC0JP0AAC-AgAAlwCZQPhVpkp0NcHSTAE")
        else:
            bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name} {message.from_user.last_name}!\n"
                                              f"We didn't recognize you. Would you like to register in the project?",
                             reply_markup=markup_2)
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEKUt5lB2nQ1DAfF_iqIA6d_e4QBchSzwACRSAAAqRUeUpWWm1f0rX_qzAE")

    @bot.message_handler(commands=['help'])
    def help(message) -> None:
        bot.send_message(message.chat.id, f"{message}")

    @bot.message_handler(commands=['my_link'])
    def my_link(message) -> None:
        bot.send_message(message.chat.id, f"Link to your telegram: https://t.me/{message.from_user.username}")

    @bot.message_handler(commands=['project_github'])
    def project_github(message) -> None:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("github.com", url="https://github.com/MothScientist/budget_control"))
        bot.send_message(message.chat.id, "Our open-source project on Github:", reply_markup=markup)

    @bot.message_handler(commands=['get_my_token'])
    def get_my_token(message) -> None:
        connection = connect_db()
        bot_db = FDataBase(connection)
        token: str = bot_db.get_token_by_tg_link("https://t.me/" + message.from_user.username)
        close_db_bot(connection)
        bot.send_message(message.chat.id, f"Your group token:")
        bot.send_message(message.chat.id, f"{token}")

    @bot.message_handler(commands=['add_income'])
    def add_income(message) -> None:
        bot.send_message(message.chat.id, f"Enter the amount of income:")
        bot.register_next_step_handler(message, process_transfer, False)

    @bot.message_handler(commands=['add_expense'])
    def add_expense(message):
        bot.send_message(message.chat.id, f"Enter the amount of expense:")
        bot.register_next_step_handler(message, process_transfer, True)

    def process_transfer(message, is_negative: bool = False) -> None:
        """
        Adds income and expense to the database. Accepts an unvalidated value,
        performs validation and enters it into the database.

        If the value == 0, then it will be regarded as False.
        :param message:
        :param is_negative: False if X > 0 (add_income), True if X < 0 (add_expense) [default=False]
        :return: None
        """
        transfer: str = message.text
        transfer: int | bool = input_number(transfer)

        if transfer:
            connection = connect_db()
            bot_db = FDataBase(connection)
            group_id: int = bot_db.get_group_id_by_tg_link("https://t.me/" + message.from_user.username)
            username: str = bot_db.get_username_by_tg_link("https://t.me/" + message.from_user.username)
            if is_negative:
                bot_db.add_monetary_transaction_to_db(f"budget_{group_id}", username, transfer*(-1))
            else:
                bot_db.add_monetary_transaction_to_db(f"budget_{group_id}", username, transfer)

            close_db_bot(connection)
            bot.send_message(message.chat.id, "Data added successfully.")

    @bot.message_handler(commands=['view_table'])
    def view_table(message) -> None:
        pass

    @bot.message_handler(commands=['registration'])
    def registration(message) -> None:

        connection = connect_db()
        bot_db = FDataBase(connection)
        res: bool | str = bot_db.get_username_by_tg_link("https://t.me/" + message.from_user.username)

        if not res:  # Checking whether the user is already registered and accidentally ended up in this menu.
            bot.send_message(message.chat.id, "Let's start registration!")
            bot.send_message(message.chat.id, "Enter your name (3-20 characters):")
            bot.register_next_step_handler(message, process_username)
        else:
            bot.send_message(message.chat.id, "You are already registered!")
            start(message)

    def process_username(message):
        username: str = message.text
        connection = connect_db()
        bot_db = FDataBase(connection)

        if (3 <= len(username) <= 20 and
                not re.match(r'^[$\\/\\-_#@&*№!:;\'",`~]', username) and
                not bot_db.get_id_by_username_or_tg_link(username=username)):
            bot.send_message(message.chat.id, "Accepted the data! Let's continue!")
            bot.send_message(message.chat.id, "Enter your password (4-128 characters):")
            bot.register_next_step_handler(message, process_psw, username)
        else:
            start(message)

        close_db_bot(connection)

    def process_psw(message, username: str):
        psw: str = message.text

        if 4 <= len(psw) <= 128:
            psw_salt: str = get_salt()
            psw: str = getting_hash(psw, psw_salt)

            bot.send_message(message.chat.id, "Well done! There's still a little time left!")
            bot.send_message(message.chat.id, "Token (if you are adding to an existing family, otherwise send 'none')")
            bot.register_next_step_handler(message, process_token, username, psw, psw_salt)
        else:
            start(message)

    def process_token(message, username: str, psw_hash: str, psw_salt: str):

        token: str = message.text
        if len(token) <= 5:
            connection = connect_db()
            bot_db = FDataBase(connection)
            tg_link: str = "https://t.me/" + message.from_user.username
            user_token: str = bot_db.create_new_group(tg_link)
            group_id: int = token_validator(user_token)  # error
            if bot_db.add_user_to_db(username, psw_salt, psw_hash, group_id, tg_link):
                close_db_bot(connection)
                create_table_group(f"budget_{group_id}")
                bot.send_message(message.chat.id, "Congratulations on registering!")
                bot.send_message(message.chat.id, "Your token:")
                bot.send_message(message.chat.id, user_token)
                start(message)
            else:
                start(message)

        elif len(token) == 32:
            connection = connect_db()
            bot_db = FDataBase(connection)
            tg_link: str = "https://t.me/" + message.from_user.username
            group_id: int = token_validator(token)  # error
            if bot_db.add_user_to_db(username, psw_salt, psw_hash, group_id, tg_link):
                close_db_bot(connection)
                bot.send_message(message.chat.id, "Congratulations on registering!")
                start(message)
            else:
                start(message)

        else:
            start(message)

    @bot.message_handler(content_types=['text'])
    def text(message) -> None:

        if message.text == "❓ Help":
            help(message)

        elif message.text == "📎 Link to GitHub":
            project_github(message)

        elif message.text == "💻 My Telegram link":
            my_link(message)

        elif message.text == "🤡 I want to register":
            registration(message)

        elif message.text == "🔐 Get my token":
            get_my_token(message)

        elif message.text == "📖 View table":
            view_table(message)

        elif message.text == "📈 Add income":
            add_income(message)

        elif message.text == "📉 Add expense":
            add_expense(message)

    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
