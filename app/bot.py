from os import getenv
from dotenv import load_dotenv
from source.password_hashing import getting_hash, get_salt
import asyncio
from datetime import date

import telebot
from telebot import types

from database_control import DatabaseQueries, connect_db, close_db_main, create_table_group

from csv_file_generation_and_deletion import create_csv_file, delete_csv_file

from validators.registration import username_validation, password_validation
from validators.description import description_validation
from validators.number import number_validation
from validators.date import date_validation
from secrets import compare_digest

from log_settings import setup_logger
from time_checking import timeit

load_dotenv()  # Load environment variables from .env file

bot_token = getenv("BOT_TOKEN")  # Get the bot token from an environment variable
bot = telebot.TeleBot(bot_token)

logger_bot = setup_logger("logs/BotLog.log", "bot_logger")


@bot.message_handler(commands=['start'])
def start(message) -> None:
    # check user in our project
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    telegram_id: int = message.from_user.id
    res: str = bot_db.get_username_by_telegram_id(telegram_id)

    if res:
        bot_db.update_user_last_login(res)
        # to send a sticker in .webp format no larger than 512x512 pixel
        # sticker = open("H:\telebot\stickers\stick_name.webp", "rb")
        # bot.send_sticker(message.chat.id, sticker)
        bot.send_message(message.chat.id, f"Hello, {res}!\nWe recognized you. Welcome!")
        bot.send_sticker(message.chat.id,
                         "CAACAgIAAxkBAAEKUtplB2lgxLm33sr3QSOP0WICC0JP0AAC-AgAAlwCZQPhVpkp0NcHSTAE")
        reply_menu_buttons_register(message)
        logger_bot.info(f"Bot start with registration: username: {res}, tg id={telegram_id}.")
    else:
        bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name}!\n"
                                        f"We didn't recognize you. Would you like to register in the project?")
        bot.send_sticker(message.chat.id,
                         "CAACAgIAAxkBAAEKUt5lB2nQ1DAfF_iqIA6d_e4QBchSzwACRSAAAqRUeUpWWm1f0rX_qzAE")
        reply_menu_buttons_not_register(message)
        logger_bot.info(f"Bot start without registration: tg id={telegram_id}.")

    close_db_main(connection)


def reply_menu_buttons_register(message):
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton("❓ Help")
    btn2 = types.KeyboardButton("📎 Link to GitHub")
    btn3 = types.KeyboardButton("🔐 Get my token")
    btn4 = types.KeyboardButton("💵 Table manage")
    btn5 = types.KeyboardButton("💻 Group settings")
    btn6 = types.KeyboardButton("⭐ Premium")
    markup_1.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, "Click the button you need :)", reply_markup=markup_1)


def reply_menu_buttons_not_register(message):
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("❓ Help")
    btn2 = types.KeyboardButton("📎 Link to GitHub")
    btn3 = types.KeyboardButton("💻 My Telegram ID")
    btn4 = types.KeyboardButton("🤡 I want to register")
    markup_1.add(btn1, btn2, btn3, btn4)

    bot.send_message(message.chat.id, "Click the button you need :)", reply_markup=markup_1)


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


def group_settings_get_buttons(message):
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🌍 Group users")
    btn2 = types.KeyboardButton("🗑️ Delete my account")
    btn3 = types.KeyboardButton("🚫 Delete group")
    btn4 = types.KeyboardButton("🔑 Change owner")
    btn5 = types.KeyboardButton("🤖 Delete user")
    btn6 = types.KeyboardButton("↩️ Back")
    markup_1.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, "Click the button you need (Group settings)", reply_markup=markup_1)


def reply_buttons(message):
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    res: str = bot_db.get_username_by_telegram_id(message.from_user.id)
    close_db_main(connection)
    if res:
        reply_menu_buttons_register(message)
    else:
        reply_menu_buttons_not_register(message)


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


@bot.message_handler(commands=['premium'])
def premium(message):
    bot.send_message(message.chat.id, "This functionality is currently under development!")


def get_my_token(message) -> None:
    telegram_id: int = message.from_user.id
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    token: str = bot_db.get_token_by_telegram_id(telegram_id)
    close_db_main(connection)
    token: str = token if token else "unknown"
    bot.send_message(message.chat.id, "Your group token:")
    bot.send_message(message.chat.id, f"{token}")


def add_income(message) -> None:
    res: bool = check_user_registration(message)
    if res:  # user authorization check
        bot.send_message(message.chat.id, "Enter the value of income:")
        bot.register_next_step_handler(message, process_add_date_for_transfer, False)


def add_expense(message):
    res: bool = check_user_registration(message)
    if res:  # user authorization check
        bot.send_message(message.chat.id, "Enter the value of expense:")
        bot.register_next_step_handler(message, process_add_date_for_transfer, True)


def process_add_date_for_transfer(message, is_negative: bool) -> None:
    """
    Adds income and expense to the database.
    Accepts an unvalidated value,
    performs validation and enters it into the database.

    If value == 0 then it will be rejected
    :param message:
    :param is_negative: False if X > 0 (add_income), True if X < 0 (add_expense)
    :return: None
    """
    value: str = message.text
    value: int = number_validation(value)
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    today_date: str = str(date.today())
    btn1 = types.KeyboardButton(f"{today_date[-2:]}/{today_date[5:7]}/{today_date[:4]}")
    markup_1.add(btn1)

    if value:
        value: int = value * (-1 if is_negative else 1)
        bot.send_message(message.chat.id, "Set the date (DD/MM/YYYY)", reply_markup=markup_1)
        bot.register_next_step_handler(message, process_add_category_for_transfer, value)
    else:
        bot.send_message(message.chat.id, "Invalid value format")


def process_add_category_for_transfer(message, value: int) -> None:
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    button_labels = ("Supermarkets", "Restaurants", "Clothes", "Medicine", "Transport", "Devices", "Education",
                     "Services", "Travel", "Housing", "Transfers", "Investments", "Hobby", "Jewelry", "Sale",
                     "Salary", "Other")
    buttons = [types.KeyboardButton(label) for label in button_labels]  # Assembling buttons from the tuple above
    markup_1.add(*buttons)

    record_date: str = message.text
    record_date_is_valid: bool = asyncio.run(date_validation(record_date))  # DD/MM/YYYY

    if record_date_is_valid:
        bot.send_message(message.chat.id, "Select category or enter your own:", reply_markup=markup_1)
        bot.register_next_step_handler(message, process_add_description_for_transfer, value, record_date)
    else:
        bot.send_message(message.chat.id, "Invalid date format")
        reply_buttons(message)


def process_add_description_for_transfer(message, value: int, record_date: str) -> None:
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    btn1 = types.KeyboardButton("No description")
    markup_1.add(btn1)
    category: str = message.text
    bot.send_message(message.chat.id, "Add description (no more than 50 characters)", reply_markup=markup_1)
    bot.register_next_step_handler(message, process_transfer_final, value, record_date, category)


def process_transfer_final(message, value: int, record_date: str, category: str) -> None:
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
    table_manage_get_buttons(message)


@timeit
def delete_record(message):
    res: bool = check_user_registration(message)
    if res:  # user authorization check
        bot.send_message(message.chat.id, "Enter the record ID:")
        bot.register_next_step_handler(message, process_delete_record)


def process_delete_record(message):
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton("❌ Delete record")
    btn2 = types.KeyboardButton("↩️ Back to menu")
    markup_1.add(btn1, btn2)
    record_id: str = message.text
    record_id: int = number_validation(record_id)

    if record_id:
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        telegram_id: int = message.from_user.id
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        if group_id and bot_db.check_id_is_exist(group_id, record_id):
            bot_db.delete_budget_entry_by_id(group_id, record_id)
            bot.send_message(message.chat.id, "Successfully!")
        else:
            bot.send_message(message.chat.id, "There is no record with this ID", reply_markup=markup_1)
        close_db_main(connection)
    else:
        bot.send_message(message.chat.id, "Invalid value", reply_markup=markup_1)


@timeit
def registration(message) -> None:
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    res: str = bot_db.get_username_by_telegram_id(message.from_user.id)
    close_db_main(connection)
    if not res:  # Checking whether the user is already registered and accidentally ended up in this menu.
        bot.send_message(message.chat.id, "Enter your name (3-20 characters):")
        bot.register_next_step_handler(message, process_username)
    else:
        bot.send_message(message.chat.id, "You are already registered!")
        reply_buttons(message)


def process_username(message):
    username: str = message.text
    if asyncio.run(username_validation(username)):
        bot.send_message(message.chat.id, "Enter your password (8-32 characters / at least 1 number and 1 letter):")
        bot.register_next_step_handler(message, process_psw, username)
    else:
        bot.send_message(message.chat.id, "Invalid username format or this username already exists!")


def process_psw(message, username: str):
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("None")
    markup_1.add(btn1)

    psw: str = message.text
    if asyncio.run(password_validation(psw)):
        psw_salt: str = get_salt()
        psw: str = getting_hash(psw, psw_salt)
        bot.send_message(message.chat.id, "Enter group token\nIf you don't have one, enter 'None'",
                         reply_markup=markup_1)
        bot.register_next_step_handler(message, process_token, username, psw, psw_salt)
    else:
        bot.send_message(message.chat.id, "Invalid password format!")
        reply_buttons(message)


def process_token(message, username: str, psw_hash: str, psw_salt: str):
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("None")
    markup_1.add(btn1)

    token: str = message.text
    telegram_id: int = message.from_user.id
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    if compare_digest(token, "None"):
        user_token: str = bot_db.create_new_group(telegram_id)
        # There is a chance to return False if an error occurred while working with the database
        if user_token:
            group_id: int = bot_db.get_group_id_by_token(user_token)
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
        group_id: int = bot_db.get_group_id_by_token(token)
        group_not_full: bool = bot_db.check_limit_users_in_group(group_id)
        if group_not_full:  # if the group doesn't exist, group_not_full will be set to False in the try/except
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
        bot.send_message(message.chat.id, "This is invalid token format")
        logger_bot.info(f"Authorization attempt with incorrect token format. Token: {token}, ID: {telegram_id}")
        reply_buttons(message)
    close_db_main(connection)


@timeit
def view_table(message) -> None:
    telegram_id: int = message.from_user.id
    res: bool = check_user_registration(message, telegram_id=telegram_id)
    if res:  # user authorization check
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        # the last entry will be at the bottom of the message <- [::-1] reverses the list
        data: list = bot_db.select_data_for_household_table(int(group_id), 10)[::-1]
        close_db_main(connection)
        if data:
            bot.send_message(message.chat.id,
                             '\n'.join([f"ID: {item[0]}\n"
                                        f"Total: {item[1]}\n"
                                        f"Username: {item[2]}\n"
                                        f"Transfer: {item[3]}\n"
                                        f"Category: {item[4]}\n"
                                        f"DateTime: {item[5]}\n"
                                        f"Description: {item[6]}\n\n"
                                        for item in data]))
        else:
            bot.send_message(message.chat.id, "Your records table is empty")
        logger_bot.info(f"ID: {telegram_id} - view_table")


@timeit
def get_csv(message):
    telegram_id: int = message.from_user.id
    res: bool = check_user_registration(message, telegram_id=telegram_id)
    if res:  # user authorization check
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        close_db_main(connection)
        try:
            create_csv_file(group_id)
            bot.send_document(message.chat.id, open(f"csv_tables/table_{group_id}.csv", 'rb'))
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Error. Try again later or report the problem to technical support.")
            logger_bot.error(f"CSV FileNotFoundError. ID: {telegram_id}, group: {group_id}")
        else:
            delete_csv_file(group_id)
            logger_bot.info(f"CSV: SUCCESS. ID: {telegram_id}, group: {group_id}")


@timeit
def get_group_users(message):
    telegram_id: int = message.from_user.id
    res: bool = check_user_registration(message, telegram_id=telegram_id)
    if res:
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        group_users_list: list = bot_db.get_group_users(group_id)
        group_owner: str = bot_db.get_group_owner_username(group_id)
        close_db_main(connection)
        group_users_str: str = '\n'.join(f"{user} (owner)" if user == group_owner
                                         else f"{user}" for user in group_users_list)
        bot.send_message(message.chat.id, group_users_str)


@timeit
def change_owner(message):
    telegram_id: int = message.from_user.id
    res: bool = check_user_registration(message, telegram_id=telegram_id)
    if res:
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        group_owner: str = bot_db.get_group_owner_username(group_id)
        username: str = bot_db.get_username_by_telegram_id(telegram_id)
        if group_owner == username:
            group_users_list: list = bot_db.get_group_users(group_id)
            if len(group_users_list) == 1:
                bot.send_message(message.chat.id, "There is only 1 member in this group.")
            else:
                group_users_str: str = '\n'.join(f"{user}" for user in group_users_list if user != group_owner)
                bot.send_message(message.chat.id, f"Write below the name of the user (from the list) you want "
                                                  f"to assign as the owner of the group: \n{group_users_str}")
                bot.register_next_step_handler(message, process_change_owner, group_id, group_users_list)
        else:
            bot.send_message(message.chat.id, "Only the group owner can change the group owner.")
        close_db_main(connection)


def process_change_owner(message, group_id: int, group_users_list: list):
    new_owner: str = message.text
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    user_is_owner: bool = bot_db.check_username_is_group_owner(new_owner, group_id)

    if user_is_owner:
        bot.send_message(message.chat.id, "This is the current owner of the group.")
    elif new_owner in group_users_list:
        if bot_db.update_group_owner(new_owner, group_id):
            bot.send_message(message.chat.id, "Group owner has been changed.")
            logger_bot.info(f"Group owner changed: group #{group_id}, new owner: {new_owner}")
        else:
            bot.send_message(message.chat.id, "An error occurred while changing the group owner.")
    else:
        bot.send_message(message.chat.id, "Check the correct spelling of the username.\n"
                                          "There is no such username in the group.")
    close_db_main(connection)


@timeit
def delete_account(message):
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton("👍 YES")
    btn2 = types.KeyboardButton("👎 NO")
    markup_1.add(btn1, btn2)
    telegram_id: int = message.from_user.id
    res: bool = check_user_registration(message, telegram_id=telegram_id)
    if res:
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        username: str = bot_db.get_username_by_telegram_id(telegram_id)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        user_is_owner: bool = bot_db.check_username_is_group_owner(username, group_id)
        close_db_main(connection)
        if not user_is_owner:
            bot.send_message(message.chat.id, "Are you sure you want to remove the account?",
                             reply_markup=markup_1)
            bot.register_next_step_handler(message, process_delete_account, username)
        else:
            bot.send_message(message.chat.id, "You are the owner of the group: either transfer the rights to "
                                              "manage another participant, or delete the group.")


def process_delete_account(message, username: str):
    user_choice: str = message.text
    if user_choice == "👍 YES":
        markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton("Start")
        markup_1.add(btn1)

        bot.send_message(message.chat.id, "We respect your choice, thanks to be with us!")
        bot.send_message(message.chat.id, "[===> In progress ===>]")

        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        bot_db.delete_user_from_project(username)
        close_db_main(connection)

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


@timeit
def delete_user(message):
    telegram_id: int = message.from_user.id
    res: bool = check_user_registration(message, telegram_id=telegram_id)
    if res:
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        group_owner: str = bot_db.get_group_owner_username(group_id)
        username: str = bot_db.get_username_by_telegram_id(telegram_id)
        user_is_owner: bool = bot_db.check_username_is_group_owner(username, group_id)
        if user_is_owner:
            group_users_list: list = bot_db.get_group_users(group_id)
            if len(group_users_list) == 1:
                bot.send_message(message.chat.id, "There are no users in the group except you.\n"
                                                  "If you want to delete your account, "
                                                  "select the appropriate item in the menu.")
            else:
                group_users_str: str = '\n'.join(f"{user}" for user in group_users_list if user != group_owner)
                bot.send_message(message.chat.id, f"Below write the name of the user (from the list) you want "
                                                  f"to remove from the group:\n{group_users_str}")
                bot.register_next_step_handler(message, process_delete_user, group_id, group_users_list)
        else:
            bot.send_message(message.chat.id, "Only the group owner can delete users.")
        close_db_main(connection)


@timeit
def process_delete_user(message, group_id: int, group_users_list: list):
    username_to_delete: str = message.text
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    user_is_owner: bool = bot_db.check_username_is_group_owner(username_to_delete, group_id)

    if user_is_owner:
        bot.send_message(message.chat.id, "This is the current owner of the group.")
    elif username_to_delete in group_users_list:
        if bot_db.delete_user_from_project(username_to_delete):
            bot.send_message(message.chat.id, "The user has been successfully removed from the group.")
            logger_bot.info(f"User deleted by group owner: user: {username_to_delete}, group #{group_id}")
        else:
            bot.send_message(message.chat.id, "An error occurred while deleting a user.")
    else:
        bot.send_message(message.chat.id, "Check the correct spelling of the username.\n"
                                          "There is no such username in the group.")
    close_db_main(connection)


@timeit
def delete_group(message):
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton("🌧️ YES")
    btn2 = types.KeyboardButton("🌤️ NO")
    markup_1.add(btn1, btn2)

    telegram_id: int = message.from_user.id
    res: bool = check_user_registration(message, telegram_id=telegram_id)
    if res:
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        username: str = bot_db.get_username_by_telegram_id(telegram_id)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        bot_db.update_user_last_login(username)
        user_is_owner: bool = bot_db.check_username_is_group_owner(username, group_id)
        if user_is_owner:
            bot.send_message(message.chat.id, "Are you sure you want to delete the group?\n"
                                              "(A table and all participants will be deleted)",
                             reply_markup=markup_1)
            bot.register_next_step_handler(message, process_delete_group, group_id)
        else:
            bot.send_message(message.chat.id, "The group can only be removed by its owner"
                                              " - contact the owner of the group, or delete the account.")
        close_db_main(connection)


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


# checking whether the user is registered in the project
# (since he may accidentally end up in a menu that is intended only for registered users)
def check_user_registration(message, telegram_id: int = 0) -> bool:
    # if the telegram_id has already been specified, then there is no point in calling
    # the function again to determine it, and it is easier to pass it as a parameter
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    if not telegram_id:  # if the telegram_id is not transmitted, then we receive it
        telegram_id: int = message.from_user.id
    res: str = bot_db.get_username_by_telegram_id(telegram_id)
    if res:
        bot_db.update_user_last_login(res)
        close_db_main(connection)
        return True
    close_db_main(connection)
    bot.send_message(message.chat.id, "You are not register.")
    bot.send_sticker(message.chat.id, "CAACAgQAAxkBAAEKeMJlIU2d3ci3xJWpzQyWm1lamvtqpQACkAADzjkIDQRZLZcg00SoMAQ")
    logger_bot.info(f"Unregistered user interaction. ID: {telegram_id}")
    return False


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
    elif message.text == "⭐ Premium":
        premium(message)
    elif message.text == "🌍 Group users":
        get_group_users(message)
    elif message.text == "🗑️ Delete my account":
        delete_account(message)
    elif message.text == "🚫 Delete group":
        delete_group(message)
    elif message.text == "🔑 Change owner":
        change_owner(message)
    elif message.text == "🤖 Delete user":
        delete_user(message)
    elif "↩️" in message.text:
        reply_buttons(message)
    else:
        bot.send_message(message.chat.id, "I don't understand you :(")


bot.polling(none_stop=True)
