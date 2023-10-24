from os import getenv
from dotenv import load_dotenv
from password_hashing import getting_hash, get_salt
import asyncio

# Telegram bot
import telebot
from telebot import types

# Database
from database_control import DatabaseQueries, connect_db, close_db_main, create_table_group

# CSV files
from csv_file_generation_and_deletion import create_csv_file, delete_csv_file

# Validators
from validators.registration import username_validation, password_validation
from validators.description import description_validation
from validators.correction_number import correction_number
from validators.category import category_validation
from validators.date import date_validation
from validators.token import token_validation
from secrets import compare_digest

# Logging
from log_settings import setup_logger

# Timeit decorator
from time_checking import timeit

# Date
from datetime import date


def main():

    load_dotenv()  # Load environment variables from .env file

    bot_token = getenv("BOT_TOKEN")  # Get the bot token from an environment variable
    bot = telebot.TeleBot(bot_token)

    logger_bot = setup_logger("logs/BotLog.log", "bot_logger")

    @bot.message_handler(commands=['start'])
    def start(message) -> None:
        # Buttons
        markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        markup_2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("❓ Help")
        btn2 = types.KeyboardButton("📎 Link to GitHub")
        btn3 = types.KeyboardButton("💻 My Telegram ID")
        btn4 = types.KeyboardButton("🤡 I want to register")
        btn5 = types.KeyboardButton("🔐 Get my token")
        btn6 = types.KeyboardButton("💵 Table manage")
        btn7 = types.KeyboardButton("💻 Group settings")
        markup_1.add(btn1, btn2, btn5, btn6, btn7)
        markup_2.add(btn1, btn2, btn3, btn4)

        # check user in our project
        connection = connect_db()
        bot_db = DatabaseQueries(connection)

        telegram_id: int = message.from_user.id

        res: str = bot_db.get_username_by_telegram_id(telegram_id)

        if res:
            bot_db.update_user_last_login(res)

            # to send a sticker from a car in .webp format no larger than 512x512 pixel
            # sticker = open("D:\\telebot\\stickers\\stick_name.webp)", "rb")
            # bot.send_sticker(message.chat.id, sticker)

            bot.send_message(message.chat.id, f"Hello, {res}!\nWe recognized you. Welcome!", reply_markup=markup_1)
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEKUtplB2lgxLm33sr3QSOP0WICC0JP0AAC-AgAAlwCZQPhVpkp0NcHSTAE")
            logger_bot.info(f"Bot start with registration: username: {res}, tg id={telegram_id}.")
        else:
            bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}!\n"
                                            f"We didn't recognize you. Would you like to register in the project?",
                             reply_markup=markup_2)
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEKUt5lB2nQ1DAfF_iqIA6d_e4QBchSzwACRSAAAqRUeUpWWm1f0rX_qzAE")
            logger_bot.info(f"Bot start without registration: tg id={telegram_id}.")

        close_db_main(connection)

    def reply_menu_buttons_register(message):
        markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton("❓ Help")
        btn2 = types.KeyboardButton("📎 Link to GitHub")
        btn3 = types.KeyboardButton("🔐 Get my token")
        btn4 = types.KeyboardButton("💵 Table manage")
        btn5 = types.KeyboardButton("💻 Group settings")
        markup_1.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, "Click the button you need :)", reply_markup=markup_1)

    def reply_menu_buttons_not_register(message):
        markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        btn1 = types.KeyboardButton("❓ Help")
        btn2 = types.KeyboardButton("📎 Link to GitHub")
        btn3 = types.KeyboardButton("💻 My Telegram ID")
        btn4 = types.KeyboardButton("🤡 I want to register")

        markup_1.add(btn1, btn2, btn3, btn4)

        bot.send_message(message.chat.id, "Click the button you need :)", reply_markup=markup_1)

    @bot.message_handler(commands=['table_manage_get_buttons'])
    def table_manage_get_buttons(message):
        markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("📖 View table")
        btn2 = types.KeyboardButton("📈 Add income")
        btn3 = types.KeyboardButton("📉 Add expense")
        btn4 = types.KeyboardButton("❌ Delete record")
        btn5 = types.KeyboardButton("🗃️ Get CSV")
        btn6 = types.KeyboardButton("↩️ Back")
        markup_1.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(message.chat.id, "Click the button you need (Table manage)", reply_markup=markup_1)

    @bot.message_handler(commands=['group_settings_get_buttons'])
    def group_settings_get_buttons(message):
        markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton("🌍 Group users")
        btn2 = types.KeyboardButton("🗑️ Delete my account")
        btn3 = types.KeyboardButton("🚫 Delete group")
        btn4 = types.KeyboardButton("🔑 Change owner")
        btn5 = types.KeyboardButton(" Delete user")
        btn6 = types.KeyboardButton("↩️ Back")
        markup_1.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.send_message(message.chat.id, "Click the button you need (Group settings)", reply_markup=markup_1)

    @bot.message_handler(commands=['help'])
    def help(message) -> None:
        bot.send_message(message.chat.id, "Support information")

    @bot.message_handler(commands=['get_my_id'])
    def get_my_id(message) -> None:
        bot.send_sticker(message.chat.id,
                         "CAACAgIAAxkBAAEKWillDGfSs-fnAAGchbLPICSILmW_7yoAAiMUAAKtXgABSjhqQKnHD7SIMAQ")
        bot.send_message(message.chat.id, f"Your telegram ID: {message.from_user.id}")

    @bot.message_handler(commands=['project_github'])
    def project_github(message) -> None:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("github.com", url="https://github.com/MothScientist/budget_control"))
        bot.send_message(message.chat.id, "Our open-source project on Github:", reply_markup=markup)

    @bot.message_handler(commands=['get_my_token'])
    def get_my_token(message) -> None:
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        telegram_id: int = message.from_user.id
        token: str = bot_db.get_token_by_telegram_id(telegram_id)
        if len(token) == 0:
            # noinspection HardcodedPassword
            token: str = "unknown"
            logger_bot.info(f"Unregistered user interaction. ID: {telegram_id}")
        close_db_main(connection)
        bot.send_message(message.chat.id, "Your group token:")
        bot.send_message(message.chat.id, f"{token}")

    @bot.message_handler(commands=['add_income'])
    def add_income(message) -> None:
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        telegram_id: int = message.from_user.id
        res: str = bot_db.get_username_by_telegram_id(telegram_id)

        if res:  # user authorization check
            bot_db.update_user_last_login(res)
            close_db_main(connection)

            bot.send_message(message.chat.id, "Enter the value of income:")
            bot.register_next_step_handler(message, process_transfer, False)

        else:
            close_db_main(connection)
            bot.send_message(message.chat.id, "You are not register.")
            bot.send_sticker(message.chat.id, "CAACAgQAAxkBAAEKeMJlIU2d3ci3xJWpzQyWm1lamvtqpQACkAADzjkIDQRZLZcg00SoMAQ")
            logger_bot.info(f"Unregistered user interaction. ID: {telegram_id}")

    @bot.message_handler(commands=['add_expense'])
    def add_expense(message):
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        telegram_id: int = message.from_user.id
        res: str = bot_db.get_username_by_telegram_id(telegram_id)

        if res:  # user authorization check
            bot_db.update_user_last_login(res)
            close_db_main(connection)

            bot.send_message(message.chat.id, "Enter the value of expense:")
            bot.register_next_step_handler(message, process_transfer, True)

        else:
            close_db_main(connection)
            bot.send_message(message.chat.id, "You are not register.")
            bot.send_sticker(message.chat.id,
                             "CAACAgQAAxkBAAEKeMJlIU2d3ci3xJWpzQyWm1lamvtqpQACkAADzjkIDQRZLZcg00SoMAQ")
            logger_bot.info(f"Unregistered user interaction. ID: {telegram_id}")

    @bot.message_handler(commands=['delete_record'])
    @timeit
    def delete_record(message):
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        telegram_id: int = message.from_user.id
        res: str = bot_db.get_username_by_telegram_id(telegram_id)

        if res:  # user authorization check
            bot_db.update_user_last_login(res)
            close_db_main(connection)

            bot.send_message(message.chat.id, "Enter the record ID:")
            bot.register_next_step_handler(message, process_delete_record)

        else:
            close_db_main(connection)
            bot.send_message(message.chat.id, "You are not register.")
            bot.send_sticker(message.chat.id,
                             "CAACAgQAAxkBAAEKeMJlIU2d3ci3xJWpzQyWm1lamvtqpQACkAADzjkIDQRZLZcg00SoMAQ")
            logger_bot.info(f"Unregistered user interaction. ID: {telegram_id}")

    @bot.message_handler(commands=['view_table'])
    @timeit
    def view_table(message) -> None:
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        telegram_id: int = message.from_user.id
        username: str = bot_db.get_username_by_telegram_id(telegram_id)
        if username:  # user authorization check
            bot_db.update_user_last_login(username)
            group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)

            data: list = bot_db.select_data_for_household_table(int(group_id), 10)

            bot.send_message(message.chat.id,
                             '\n'.join([
                                           f"ID: {item[0]}\n"
                                           f"Total: {item[1]}\n"
                                           f"Username: {item[2]}\n"
                                           f"Transfer: {item[3]}\n"
                                           f"Category: {item[4]}\n"
                                           f"DateTime: {item[5]}\n"
                                           f"Description: {item[6]}\n\n"
                                           for item in data
                             ]))

            logger_bot.info(f"ID: {telegram_id} - view_table")
        else:
            bot.send_message(message.chat.id, "You are not register.")
            bot.send_sticker(message.chat.id,
                             "CAACAgQAAxkBAAEKeMJlIU2d3ci3xJWpzQyWm1lamvtqpQACkAADzjkIDQRZLZcg00SoMAQ")
            logger_bot.info(f"Unregistered user interaction. ID: {telegram_id}")
        close_db_main(connection)

    @bot.message_handler(commands=['registration'])
    @timeit
    def registration(message) -> None:

        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        res: str = bot_db.get_username_by_telegram_id(message.from_user.id)
        close_db_main(connection)

        if not res:  # Checking whether the user is already registered and accidentally ended up in this menu.
            bot.send_message(message.chat.id, "Let's start registration!")
            bot.send_message(message.chat.id, "Enter your name (3-20 characters):")
            bot.register_next_step_handler(message, process_username)
        else:
            bot.send_message(message.chat.id, "You are already registered!")
            start(message)

    @bot.message_handler(commands=['get_csv'])
    @timeit
    def get_csv(message):
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        telegram_id: int = message.from_user.id
        username: str = bot_db.get_username_by_telegram_id(telegram_id)
        if username:  # user authorization check
            bot_db.update_user_last_login(username)
            group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
            create_csv_file(group_id)
            try:
                bot.send_document(message.chat.id, open(f"csv_tables/table_{group_id}.csv", 'rb'))
                delete_csv_file(group_id)
                logger_bot.info(f"CSV: SUCCESS. ID: {telegram_id}, group: {group_id}")
            except FileNotFoundError:
                bot.send_message(message.chat.id, "Error. Try again later or report the problem to technical support.")
                logger_bot.error(f"CSV FileNotFoundError. ID: {telegram_id}, group: {group_id}")
        else:
            bot.send_message(message.chat.id, "You are not register.")
            bot.send_sticker(message.chat.id, "CAACAgQAAxkBAAEKeMJlIU2d3ci3xJWpzQyWm1lamvtqpQACkAADzjkIDQRZLZcg00SoMAQ")
            logger_bot.info(f"Unregistered user interaction. ID: {telegram_id}")

        close_db_main(connection)

    @bot.message_handler(commands=['get_group_users'])
    @timeit
    def get_group_users(message):
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        telegram_id: int = message.from_user.id
        username: str = bot_db.get_username_by_telegram_id(telegram_id)

        if username:
            bot_db.update_user_last_login(username)

            group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)

            group_id: int = group_id
            group_users_list: list = bot_db.get_group_users(group_id)
            group_owner: str = bot_db.get_group_owner_username(group_id)
            group_users_str: str = '\n'.join(f"{user} (owner)" if user == group_owner
                                             else f"{user}" for user in group_users_list)

            bot.send_message(message.chat.id, group_users_str)
        else:
            bot.send_message(message.chat.id, "You are not register.")
            bot.send_sticker(message.chat.id, "CAACAgQAAxkBAAEKeMJlIU2d3ci3xJWpzQyWm1lamvtqpQACkAADzjkIDQRZLZcg00SoMAQ")
            logger_bot.info(f"Unregistered user interaction. ID: {telegram_id}")

        close_db_main(connection)

    @bot.message_handler(commands=['delete_account'])
    @timeit
    def delete_account(message):
        markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

        btn1 = types.KeyboardButton("👍 YES")
        btn2 = types.KeyboardButton("👎 NO")

        markup_1.add(btn1, btn2)

        connection = connect_db()
        bot_db = DatabaseQueries(connection)

        telegram_id: int = message.from_user.id
        username: str = bot_db.get_username_by_telegram_id(telegram_id)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)

        if username and group_id:
            username: str = username
            group_id: int = group_id

            bot_db.update_user_last_login(username)
            user_is_owner: bool = bot_db.check_username_is_group_owner(username, group_id)
            close_db_main(connection)

            if not user_is_owner:
                bot.send_message(message.chat.id, "Are you sure you want to remove the account?",
                                 reply_markup=markup_1)
                bot.register_next_step_handler(message, process_delete_account, username)

            else:
                bot.send_message(message.chat.id,"You are the owner of the group: "
                                 "either transfer the rights to manage another participant, or delete the group.")
        else:
            close_db_main(connection)
            bot.send_message(message.chat.id, "You are not register.")
            bot.send_sticker(message.chat.id, "CAACAgQAAxkBAAEKeMJlIU2d3ci3xJWpzQyWm1lamvtqpQACkAADzjkIDQRZLZcg00SoMAQ")
            logger_bot.info(f"Unregistered user interaction. ID: {telegram_id}")

    @bot.message_handler(commands=['delete_group'])
    @timeit
    def delete_group(message):
        markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        btn1 = types.KeyboardButton("🌧️ YES")
        btn2 = types.KeyboardButton("🌤️ NO")
        markup_1.add(btn1, btn2)

        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        telegram_id: int = message.from_user.id
        username: str = bot_db.get_username_by_telegram_id(telegram_id)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)

        if username and group_id:
            username: str = username
            group_id: int = group_id
            bot_db.update_user_last_login(username)
            user_is_owner: bool = bot_db.check_username_is_group_owner(username, group_id)
            close_db_main(connection)

            if user_is_owner:
                bot.send_message(message.chat.id, "Are you sure you want to delete the group?\n"
                                                  "(A table and all participants will be deleted)",
                                 reply_markup=markup_1)
                bot.register_next_step_handler(message, process_delete_group, group_id)
            else:
                bot.send_message(message.chat.id, "The group can only be removed by its owner"
                                                  " - contact the owner of the group, or delete the account.")
        else:
            close_db_main(connection)
            bot.send_message(message.chat.id, "You are not register.")
            bot.send_sticker(message.chat.id, "CAACAgQAAxkBAAEKeMJlIU2d3ci3xJWpzQyWm1lamvtqpQACkAADzjkIDQRZLZcg00SoMAQ")
            logger_bot.info(f"Unregistered user interaction. ID: {telegram_id}")

    @bot.message_handler(commands=['change_owner'])
    @timeit
    def change_owner(message):
        telegram_id: int = message.from_user.id
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)

        if group_id:
            current_owner: str = bot_db.get_group_owner_username(group_id)
            username: str = bot_db.get_username_by_telegram_id(telegram_id)
            close_db_main(connection)
            if current_owner == username:
                bot.send_message(message.chat.id, "Write below the name of the user (from the list)"
                                              " you want to assign as the owner of the group:")
                get_group_users(message)
                bot.register_next_step_handler(message, process_change_owner, group_id)
            else:
                bot.send_message(message.chat.id, "Only the current owner can change the group owner.")

        else:
            close_db_main(connection)
            bot.send_message(message.chat.id, "You are not register.")
            bot.send_sticker(message.chat.id, "CAACAgQAAxkBAAEKeMJlIU2d3ci3xJWpzQyWm1lamvtqpQACkAADzjkIDQRZLZcg00SoMAQ")
            logger_bot.info(f"Unregistered user interaction. ID: {telegram_id}")

    def process_change_owner(message, group_id: int):
        new_owner: str = message.text
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        group_users: list = bot_db.get_group_users(group_id)

        if new_owner in group_users:
            if bot_db.update_group_owner(new_owner, group_id):
                bot.send_message(message.chat.id, "Group owner has been changed.")
            else:
                bot.send_message(message.chat.id, "An error occurred while changing the group owner.")
        else:
            bot.send_message(message.chat.id, "Check the correct spelling of the username.\n"
                                              "There is no such username in the group.")
        close_db_main(connection)

    def process_delete_account(message, username: str):
        user_choice: str = message.text

        if user_choice == "👍 YES":
            bot.send_message(message.chat.id, "We respect your choice, thanks to be with us!")
            bot.send_message(message.chat.id, "[===> In progress ===>]")

            connection = connect_db()
            bot_db = DatabaseQueries(connection)
            bot_db.delete_user_from_project(username)
            close_db_main(connection)

            markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton("Start")
            markup_1.add(btn1)

            bot.send_message(message.chat.id, "Your account is completely deleted!", reply_markup=markup_1)
            logger_bot.info(f"User deleted the account. ID: {message.from_user.id}")

        elif user_choice == "👎 NO":
            bot.send_message(message.chat.id, "We are glad that you stay with us!")
            start(message)

        else:
            bot.send_message(message.chat.id, "Your message is not clear to us, "
                                              "please, when choosing, use the buttons at the bottom of the screen.")
            start(message)
            logger_bot.info(f"Unrecognized message when deleting an account. "
                            f"ID: {message.from_user.id}, message: {user_choice}")

    def process_delete_group(message, group_id: int):
        user_choice: str = message.text

        if user_choice == "🌧️ YES":
            bot.send_message(message.chat.id, "We respect your choice, thanks to be with us!")
            bot.send_message(message.chat.id, "[===> In progress ===>]")

            connection = connect_db()
            bot_db = DatabaseQueries(connection)
            bot_db.delete_group_with_users(group_id)
            close_db_main(connection)

            markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton("Start")
            markup_1.add(btn1)

            bot.send_message(message.chat.id, "The group and users are completely deleted!", reply_markup=markup_1)
            logger_bot.info(f"User deleted the group. ID: {message.from_user.id}, group #{group_id}")

        elif user_choice == "🌤️ NO":
            bot.send_message(message.chat.id, "We are glad that you stay with us!")
            start(message)

        else:
            bot.send_message(message.chat.id, "Your message is not clear to us, "
                                              "please, when choosing, use the buttons at the bottom of the screen.")
            start(message)
            logger_bot.info(f"Unrecognized message when deleting group. "
                            f"ID: {message.from_user.id}, message: {user_choice}, group #{group_id}")

    def process_delete_record(message):
        record_id: str = message.text
        record_id: int = correction_number(record_id)

        if record_id:
            connection = connect_db()
            bot_db = DatabaseQueries(connection)
            telegram_id: int = message.from_user.id
            group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
            if group_id and bot_db.check_id_is_exist(group_id, record_id):
                bot_db.delete_budget_entry_by_id(group_id, record_id)
                bot.send_message(message.chat.id, "Successfully.")
            else:
                bot.send_message(message.chat.id, "There is no record with this ID.")
            close_db_main(connection)
        else:
            bot.send_message(message.chat.id, "Invalid value.")

    def process_transfer(message, is_negative: bool = False) -> None:
        """
        Adds income and expense to the database. Accepts an unvalidated value,
        performs validation and enters it into the database.

        If the value == 0, then it will be regarded as False.
        :param message:
        :param is_negative: False if X > 0 (add_income), True if X < 0 (add_expense) [default=False]
        :return: None
        """
        value: str = message.text
        value: int = correction_number(value)
        markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        today_date: str = str(date.today())
        btn1 = types.KeyboardButton(f"{today_date[-2:]}/{today_date[5:7]}/{today_date[:4]}")
        markup_1.add(btn1)

        if value:
            if is_negative:
                value: int = value*(-1)
            else:
                value: int = value
            bot.send_message(message.chat.id, "Set the date (DD/MM/YYYY)", reply_markup=markup_1)
            bot.register_next_step_handler(message, process_add_date_for_transfer, value)
        else:
            bot.send_message(message.chat.id, "Invalid date format")
            reply_menu_buttons_register(message)

    def process_add_date_for_transfer(message, value: int) -> None:
        markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
        btn1 = types.KeyboardButton("Supermarkets")
        btn2 = types.KeyboardButton("Restaurants")
        btn3 = types.KeyboardButton("Clothes")
        btn4 = types.KeyboardButton("Medicine")
        btn5 = types.KeyboardButton("Transport")
        btn6 = types.KeyboardButton("Devices")
        btn7 = types.KeyboardButton("Education")
        btn8 = types.KeyboardButton("Services")
        btn9 = types.KeyboardButton("Travel")
        btn10 = types.KeyboardButton("Housing")
        btn11 = types.KeyboardButton("Transfers")
        btn12 = types.KeyboardButton("Investments")
        btn13 = types.KeyboardButton("Hobby")
        btn14 = types.KeyboardButton("Jewelry")
        btn15 = types.KeyboardButton("Sale")
        btn16 = types.KeyboardButton("Salary")
        btn17 = types.KeyboardButton("Other")
        markup_1.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12, btn13, btn14,
                     btn15, btn16, btn17)

        record_date: str = message.text
        today_date: str = str(date.today())
        if record_date != f"{today_date[-2:]}/{today_date[5:7]}/{today_date[:4]}":
            record_date_is_valid: bool = asyncio.run(date_validation(record_date))
        else:
            record_date_is_valid: bool = True

        if record_date_is_valid:
            record_date: str = f"{record_date[-2:]}/{record_date[5:7]}/{record_date[:4]}"  # DD/MM/YYYY
            bot.send_message(message.chat.id, "Select the required category", reply_markup=markup_1)
            bot.register_next_step_handler(message, process_add_category_for_transfer, value, record_date)
        else:
            bot.send_message(message.chat.id, "Invalid date format")
            reply_menu_buttons_register(message)

    def process_add_category_for_transfer(message, value: int, record_date: str) -> None:
        markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
        btn1 = types.KeyboardButton("No description")
        markup_1.add(btn1)
        category: str = message.text
        category_is_valid: bool = category_validation(category)
        if category_is_valid:
            bot.send_message(message.chat.id, "Add description (no more than 50 characters)", reply_markup=markup_1)
            bot.register_next_step_handler(message, process_add_description_for_transfer, value, record_date, category)
        else:
            bot.send_message(message.chat.id, "Invalid category format")
            reply_menu_buttons_register(message)

    def process_add_description_for_transfer(message, value: int, record_date: str, category: str) -> None:
        description: str = message.text
        description_is_valid: bool = description_validation(description)
        if description_is_valid:
            if description == "No description":
                description: str = ""
            connection = connect_db()
            bot_db = DatabaseQueries(connection)
            telegram_id: int = message.from_user.id
            username: str = bot_db.get_username_by_telegram_id(telegram_id)
            bot_db.add_monetary_transaction_to_db(username, value, record_date, category, description)
            close_db_main(connection)
            bot.send_message(message.chat.id, "Entry added successfully!")
        else:
            bot.send_message(message.chat.id, "Invalid value")

        reply_menu_buttons_register(message)

    def process_username(message):
        username: str = message.text
        if asyncio.run(username_validation(username)):
            bot.send_message(message.chat.id, "Accepted the data! Let's continue!")
            bot.send_message(message.chat.id, "Enter your password (8-32 characters / at least 1 number and 1 letter):")
            bot.register_next_step_handler(message, process_psw, username)
        else:
            bot.send_message(message.chat.id, "Invalid username format or this username already exists!")
            reply_menu_buttons_not_register(message)

    def process_psw(message, username: str):
        markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton("None")
        markup_1.add(btn1)
        psw: str = message.text
        if asyncio.run(password_validation(psw)):
            psw_salt: str = get_salt()
            psw: str = getting_hash(psw, psw_salt)
            bot.send_message(message.chat.id, "Well done! There's still a little time left!")
            bot.send_message(message.chat.id, "Token (if you have it (32 characters), otherwise send 'None')",
                             reply_markup=markup_1)
            bot.register_next_step_handler(message, process_token, username, psw, psw_salt)
        else:
            bot.send_message(message.chat.id, "Invalid password format!")
            reply_menu_buttons_not_register(message)

    def process_token(message, username: str, psw_hash: str, psw_salt: str):
        token: str = message.text
        telegram_id: int = message.from_user.id
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        if compare_digest(token, "None"):
            user_token: str = bot_db.create_new_group(telegram_id)
            # There is a chance to return False if an error occurred while working with the database
            if user_token:
                group_id: int = token_validation(user_token)

                if bot_db.add_user_to_db(username, psw_salt, psw_hash, group_id, telegram_id):
                    create_table_group(f"budget_{group_id}")
                    bot.send_message(message.chat.id, "Congratulations on registering!")
                    bot.send_sticker(message.chat.id,
                                     "CAACAgIAAxkBAAEKWitlDGgsUhrqGudQPNuk-nI8yiz53wACsRcAAlV9AUqXI5lmIbo_TzAE")
                    bot.send_message(message.chat.id, "Your token:")
                    bot.send_message(message.chat.id, user_token)
                    logger_bot.info(f"New user (new group): ID: {telegram_id}, group: {group_id}")
                    reply_menu_buttons_register(message)
                else:
                    bot.send_message(message.chat.id, "Error creating a new user. Contact technical support!")
                    logger_bot.error(f"Error adding new user to database: ID: {telegram_id}, username: {username}, "
                                     f"psw salt: {psw_salt}, psw hash: {psw_hash}, group id: {group_id}")
                    reply_menu_buttons_not_register(message)
            else:
                bot.send_message(message.chat.id, "Error creating a new user. Contact technical support!")
                logger_bot.error(f"Error adding new user to database: ID: {telegram_id}, username: {username}, "
                                 f"psw salt: {psw_salt}, psw hash: {psw_hash}")
                reply_menu_buttons_not_register(message)
        elif len(token) == 32:
            telegram_id: int = message.from_user.id
            group_id: int = token_validation(token)
            group_not_full: bool = bot_db.check_limit_users_in_group(token)
            if group_id and group_not_full:
                if bot_db.add_user_to_db(username, psw_salt, psw_hash, group_id, telegram_id):
                    bot.send_message(message.chat.id, "Congratulations on registering!")
                    bot.send_sticker(message.chat.id,
                                     "CAACAgIAAxkBAAEKWitlDGgsUhrqGudQPNuk-nI8yiz53wACsRcAAlV9AUqXI5lmIbo_TzAE")
                    logger_bot.info(f"New user: ID: {telegram_id}, group: {group_id}")
                    reply_menu_buttons_register(message)
                else:
                    bot.send_message(message.chat.id, "Error creating a new user. Contact technical support!")
                    logger_bot.error(f"Error adding new user to database: ID: {telegram_id}, username: {username}, "
                                     f"psw salt: {psw_salt}, psw hash: {psw_hash}, group id: {group_id}")
            else:
                bot.send_message(message.chat.id, "There is no group with this token or it is full. "
                                                  "Contact the group members for more information, "
                                                  "or create your own group!")
                logger_bot.info(f"Trying to add to a full group: ID: {telegram_id}, group id: {group_id}")
        else:
            bot.send_message(message.chat.id, "This is not a valid token format, "
                                              "please check if it is correct or send 'None'!")
            logger_bot.info(f"Authorization attempt with incorrect token format. Token: {token}, ID: {telegram_id}")
            reply_menu_buttons_not_register(message)
        close_db_main(connection)

    @bot.message_handler(content_types=['text'])
    def text(message) -> None:
        if message.text == "Start":
            start(message)
        elif message.text == "❓ Help":
            help(message)
        elif message.text == "📎 Link to GitHub":
            project_github(message)
        elif message.text == "💻 My Telegram ID":
            get_my_id(message)
        elif message.text == "🤡 I want to register":
            registration(message)
        elif message.text == "🔐 Get my token":
            get_my_token(message)
        elif message.text == "💵 Table manage":
            table_manage_get_buttons(message)
        elif message.text == "📖 View table":
            view_table(message)
        elif message.text == "📈 Add income":
            add_income(message)
        elif message.text == "📉 Add expense":
            add_expense(message)
        elif message.text == "❌ Delete record":
            delete_record(message)
        elif message.text == "🗃️ Get CSV":
            get_csv(message)
        elif message.text == "💻 Group settings":
            group_settings_get_buttons(message)
        elif message.text == "🌍 Group users":
            get_group_users(message)
        elif message.text == "🗑️ Delete my account":
            delete_account(message)
        elif message.text == "🚫 Delete group":
            delete_group(message)
        elif message.text == "🔑 Change owner":
            change_owner(message)
        elif message.text == " Delete user":
            pass
        elif message.text == "↩️ Back":
            reply_menu_buttons_register(message)

    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
