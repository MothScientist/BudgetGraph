from os import getenv
from secrets import compare_digest
import asyncio
from datetime import datetime, UTC
from dotenv import load_dotenv


import telebot
from telebot import types

from app.database_control import DatabaseQueries, connect_db, close_db_main, create_table_group

from app.encryption import getting_hash, get_salt

from app.validation import (date_validation, number_validation, description_validation,
                            username_validation, password_validation)

from app.validation import (date_validation, value_validation, description_validation,
                            username_validation, password_validation, category_validation)  # noqa

from app.csv_file_generation_and_deletion import create_csv_file, get_file_size_kb, get_file_checksum  # noqa

from app.logger import setup_logger


load_dotenv()  # Load environment variables from .env file

bot_token = getenv("BOT_TOKEN")  # Get the bot token from an environment variable
bot = telebot.TeleBot(bot_token)  # type: ignore

logger_bot = setup_logger("logs/BotLog.log", "bot_logger")


@timeit
def reply_menu_buttons_register(message):
    user_language: str = check_user_language(message)
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton(f"❓ {get_phrase_by_language(user_language, "help")}")
    btn2 = types.KeyboardButton(f"📎 {get_phrase_by_language(user_language, "link_github")}")
    btn3 = types.KeyboardButton(f"🔐 {get_phrase_by_language(user_language, "get_my_token")}")
    btn4 = types.KeyboardButton(f"💵 {get_phrase_by_language(user_language, "table_manage")}")
    btn5 = types.KeyboardButton(f"💻 {get_phrase_by_language(user_language, "group_settings")}")
    btn6 = types.KeyboardButton(f"⭐ {get_phrase_by_language(user_language, "premium")}")
    btn7 = types.KeyboardButton(f"{get_phrase_by_language(user_language, "change_language")}")
    markup_1.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "click_need_button")} :)",
                     reply_markup=markup_1)


@timeit
def reply_menu_buttons_not_register(message):
    user_language: str = check_user_language(message)
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton(f"❓ {get_phrase_by_language(user_language, "help")}")
    btn2 = types.KeyboardButton(f"📎 {get_phrase_by_language(user_language, "link_github")}")
    btn3 = types.KeyboardButton(f"💻 {get_phrase_by_language(user_language, "my")} Telegram ID")
    btn4 = types.KeyboardButton("🤡 I want to register")
    btn5 = types.KeyboardButton(f"⭐ {get_phrase_by_language(user_language, "premium")}")
    btn6 = types.KeyboardButton(f"{get_phrase_by_language(user_language, "change_language")}")
    markup_1.add(btn1, btn2, btn3, btn4, btn5, btn6)

    bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "click_need_button")} :)",
                     reply_markup=markup_1)


@timeit
def table_manage_get_buttons(message):
    user_language: str = check_user_language(message)
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton(f"📖 {get_phrase_by_language(user_language, "view_table")}")
    btn2 = types.KeyboardButton(f"📈 {get_phrase_by_language(user_language, "add_income")}")
    btn3 = types.KeyboardButton(f"📉 {get_phrase_by_language(user_language, "add_expense")}")
    btn4 = types.KeyboardButton(f"❌ {get_phrase_by_language(user_language, "del_record")}")
    btn5 = types.KeyboardButton(f"🗃️ {get_phrase_by_language(user_language, "get_csv")}")
    btn6 = types.KeyboardButton(f"↩️ {get_phrase_by_language(user_language, "back")}")
    markup_1.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "click_need_button")} "
                                      f"({get_phrase_by_language(user_language, "table_manage")})",
                     reply_markup=markup_1)


@timeit
def group_settings_get_buttons(message):
    user_language: str = check_user_language(message)
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton(f"🌍 {get_phrase_by_language(user_language, "group_users")}")
    btn2 = types.KeyboardButton(f"🗑️ {get_phrase_by_language(user_language, "delete_account")}")
    btn3 = types.KeyboardButton(f"🚫 {get_phrase_by_language(user_language, "delete_group")}")
    btn4 = types.KeyboardButton(f"🔑 {get_phrase_by_language(user_language, "change_owner")}")
    btn5 = types.KeyboardButton(f"🤖 {get_phrase_by_language(user_language, "delete_user")}")
    btn6 = types.KeyboardButton(f"↩️ {get_phrase_by_language(user_language, "back")}")
    markup_1.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "click_need_button")} "
                                      f"({get_phrase_by_language(user_language, "group_settings")})",
                     reply_markup=markup_1)


@timeit
def reply_buttons(message):
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    res: str = bot_db.get_username_by_telegram_id(message.from_user.id)
    close_db(connection)
    if res:
        reply_menu_buttons_register(message)
    else:
        reply_menu_buttons_not_register(message)


@bot.message_handler(commands=['start'])
def start(message) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(message)
    res: bool = user_is_registered(message)
    if res:
        # to send a sticker in .webp format no larger than 512x512 pixel
        # sticker = open("H:\telebot\stickers\stick_name.webp", "rb")
        # bot.send_sticker(message.chat.id, sticker)
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "greetings")}"
                                          f" {message.from_user.first_name}!\n"
                                          f"{get_phrase_by_language(user_language, "our_user")}")
        bot.send_sticker(message.chat.id,f"{Stickers.get_sticker_by_id("id_1")}")
        reply_menu_buttons_register(message)
        logger_bot.info(f"Bot start with registration: username: {res}, tg id={telegram_id}.")
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "greetings")}"
                                          f" {message.from_user.first_name}!\n"
                                        f"{get_phrase_by_language(user_language, "unknown_user")}")
        bot.send_sticker(message.chat.id,f"{Stickers.get_sticker_by_id("id_2")}")
        reply_menu_buttons_not_register(message)
        logger_bot.info(f"Bot start without registration: tg id={telegram_id}.")


@bot.message_handler(commands=['help'])
def help(message) -> None:
    user_language: str = check_user_language(message)
    bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "support_information")}")


def get_my_id(message) -> None:
    user_language: str = check_user_language(message)
    bot.send_sticker(message.chat.id,f"{Stickers.get_sticker_by_id("id_3")}")
    bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "your")} "
                                      f"telegram ID: {message.from_user.id}")


@bot.message_handler(commands=['project_github'])
def project_github(message) -> None:
    user_language: str = check_user_language(message)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("github.com", url="https://github.com/MothScientist/budget_control"))
    bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "project_on_github")}:",
                     reply_markup=markup)


def premium(message):
    bot.send_message(message.chat.id, "soon")


def change_language(message) -> None:
    user_language: str = check_user_language(message)
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button_labels: tuple = ("English", "Español", "Русский", "Français", "Deutsch", "Islenskur")
    buttons = ([types.KeyboardButton(label) for label in button_labels] +
               [types.KeyboardButton(f"↩️ {get_phrase_by_language(user_language, "back")}")])
    markup_1.add(*buttons)
    bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "choose_language")}:",
                     reply_markup=markup_1)
    bot.register_next_step_handler(message, process_change_language)


def process_change_language(message):
    # if there is an error changing the language, this option will be used
    # if no error occurs, then this variable will be redefined in the 'if res' block
    user_language: str = check_user_language(message)

    languages = {  # preserves the order of values
        "English": "en",
        "Español": "es",
        "Русский": "ru",
        "Français": "fr",
        "Deutsch": "de",
        "Islenskur": "is"
    }
    user_lang = message.text
    telegram_id: int = message.from_user.id
    if user_lang in languages:  # Checks for language presence in dictionary keys (look Pylint C0201)
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        res: bool = bot_db.add_user_language(telegram_id, languages[user_lang])
        close_db(connection)
        if res:
            user_language: str = check_user_language(message)  # changing the user's language to a new option
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "great")}\n"
                                              f"{get_phrase_by_language(user_language, "language_changed")}")
            logger_bot.info(f"Successful language change. Telegram ID: {telegram_id}, language: {user_lang}")
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "error_change_language")}.\n"
                                              f"{get_phrase_by_language(user_language, "contact_support")}")
            logger_bot.error(f"Error language change. Telegram ID: {telegram_id}, language: {user_lang}")
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "unsupported_language")}")
        logger_bot.info(f"Invalid input: this language is not supported. Telegram ID: {telegram_id}, "
                        f"language: {user_lang}")
    reply_buttons(message)


def get_my_token(message) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(message)
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    token: str = bot_db.get_token_by_telegram_id(telegram_id)
    close_db(connection)
    token: str = token if token else f"{get_phrase_by_language(user_language, "unknown")}"
    bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "group_token")}:")
    bot.send_message(message.chat.id, f"{token}")


def add_income(message) -> None:
    user_language: str = check_user_language(message)
    res: bool = check_user_access(message)
    if res:  # user authorization check
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "enter_income")}:")
        bot.register_next_step_handler(message, process_add_date_for_transfer, False)


def add_expense(message):
    user_language: str = check_user_language(message)
    res: bool = check_user_access(message)
    if res:  # user authorization check
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "enter_expense")}:")
        bot.register_next_step_handler(message, process_add_date_for_transfer, True)


def process_add_date_for_transfer(message, is_negative: bool) -> None:
    """
    Adds income and expense to the database.
    Accepts an unvalidated value,
    performs validation and enters it into the database.

    If value == 0 then it will be rejected
    
    Args:
        message:
        is_negative (bool): False if X > 0 (add_income), True if X < 0 (add_expense)

    Returns: None
    """
    value: str = message.text
    value: int = value_validation(value)
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    today_date: str = datetime.now(UTC).strftime('%d/%m/%Y')
    user_language: str = check_user_language(message)
    btn1 = types.KeyboardButton(today_date)
    markup_1.add(btn1)

    if value:
        value: int = value * (-1 if is_negative else 1)
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "set_date")} (DD/MM/YYYY)",
                         reply_markup=markup_1)
        bot.register_next_step_handler(message, process_add_category_for_transfer, value)
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "invalid_value")}")


def process_add_category_for_transfer(message, value: int) -> None:
    user_language: str = check_user_language(message)
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    button_labels: tuple = (
        f"{get_phrase_by_language(user_language, "supermarkets")}",
        f"{get_phrase_by_language(user_language, "restaurants")}",
        f"{get_phrase_by_language(user_language, "clothes")}",
        f"{get_phrase_by_language(user_language, "medicine")}",
        f"{get_phrase_by_language(user_language, "transport")}",
        f"{get_phrase_by_language(user_language, "devices")}",
        f"{get_phrase_by_language(user_language, "education")}",
        f"{get_phrase_by_language(user_language, "services")}",
        f"{get_phrase_by_language(user_language, "travel")}",
        f"{get_phrase_by_language(user_language, "housing")}",
        f"{get_phrase_by_language(user_language, "transfer")}",
        f"{get_phrase_by_language(user_language, "investments")}",
        f"{get_phrase_by_language(user_language, "hobby")}",
        f"{get_phrase_by_language(user_language, "jewelry")}",
        f"{get_phrase_by_language(user_language, "salary")}",
        f"{get_phrase_by_language(user_language, "charity")}",
        f"{get_phrase_by_language(user_language, "other")}"
    )
    buttons: list = [types.KeyboardButton(label) for label in button_labels]  # Assembling buttons from the tuple above
    markup_1.add(*buttons)

    record_date: str = message.text
    record_date_is_valid: bool = asyncio.run(date_validation(record_date))  # DD/MM/YYYY

    if record_date_is_valid:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "select_category")}:", reply_markup=markup_1)  # noqa (E501)
        bot.register_next_step_handler(message, process_add_description_for_transfer, value, record_date)
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "invalid_date")}")
        reply_buttons(message)


def process_add_description_for_transfer(message, value: int, record_date: str) -> None:
    user_language: str = check_user_language(message)
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    btn1 = types.KeyboardButton(f"{get_phrase_by_language(user_language, "no_description")}")
    markup_1.add(btn1)
    category: str = message.text
    category_is_valid: bool = category_validation(user_language, category)

    if category_is_valid:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "add_description")}", reply_markup=markup_1)  # noqa (E501)
        bot.register_next_step_handler(message, process_transfer_final, value, record_date, category)
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "invalid_category")}")  # noqa (E501)
        reply_buttons(message)
        logger_bot.info(f"User entered an incorrect category. Category: {category}")


def process_transfer_final(message, value: int, record_date: str, category: str) -> None:
    user_language: str = check_user_language(message)
    telegram_id: int = message.from_user.id
    description: str = message.text
    description_is_valid: bool = description_validation(description)

    if description_is_valid:
        if description == f"{get_phrase_by_language(user_language, "no_description")}":
            description: str = ""
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        username: str = bot_db.get_username_by_telegram_id(telegram_id)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        last_total_sum: int = bot_db.get_last_sum_in_group(group_id)
        bot_db.add_monetary_transaction_to_db(username, group_id, value, last_total_sum, record_date, category, description)  # noqa: E501
        close_db(connection)
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "entry_add_success")}!")
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "invalid_value")}")
    table_manage_get_buttons(message)


def delete_record(message) -> None:
    user_language: str = check_user_language(message)
    res: bool = check_user_access(message)
    if res:  # user authorization check
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "entry_record_id")}:")
        bot.register_next_step_handler(message, process_delete_record)


def process_delete_record(message):
    user_language: str = check_user_language(message)
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton(f"❌ {get_phrase_by_language(user_language, "del_record")}")
    btn2 = types.KeyboardButton(f"↩️ {get_phrase_by_language(user_language, "back_to_menu")}")
    markup_1.add(btn1, btn2)
    record_id: str = message.text  # type: ignore
    record_id: int = value_validation(record_id)  # type: ignore

    if record_id:
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        telegram_id: int = message.from_user.id
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        if group_id and bot_db.check_record_id_is_exist(group_id, record_id):
            bot_db.delete_budget_entry_by_id(group_id, record_id)
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "success")}!")
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "enry_record_id_error")}", reply_markup=markup_1)  # noqa (E501)
        close_db(connection)
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "invalid_value")}", reply_markup=markup_1)  # noqa (E501)


def registration(message) -> None:
    user_language: str = check_user_language(message)
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    res: str = bot_db.get_username_by_telegram_id(message.from_user.id)
    close_db(connection)
    if not res:  # Checking whether the user is already registered and accidentally ended up in this menu.
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "enter_username")}:")
        bot.register_next_step_handler(message, process_username)
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "already_registered")}!")
        reply_buttons(message)


def process_username(message):
    user_language: str = check_user_language(message)
    username: str = message.text
    if asyncio.run(username_validation(username)):
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "enter_password")}:")
        bot.register_next_step_handler(message, process_psw, username)
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "invalid_username")}")


def process_psw(message, username: str):
    user_language: str = check_user_language(message)
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("None")
    markup_1.add(btn1)

    psw: str = message.text
    if asyncio.run(password_validation(psw)):
        psw_salt: str = get_salt()
        psw: str = getting_hash(psw, psw_salt)
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "enter_token")}\n"
                                          f"{get_phrase_by_language(user_language, "none_token")}",
                         reply_markup=markup_1)
        bot.register_next_step_handler(message, process_token, username, psw, psw_salt)
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "invalid_password_format")}")
        reply_buttons(message)


def process_token(message, username: str, psw_hash: str, psw_salt: str):
    user_language: str = check_user_language(message)
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("None")
    markup_1.add(btn1)

    token: str = message.text
    telegram_id: int = message.from_user.id
    connection = connect_db()
    bot_db = DatabaseQueries(connection)

    if token == "None":  # noqa (PW100) - I don’t think there is any need for time attack protection here
        new_group_token: str = bot_db.create_new_group(telegram_id)
        # There is a chance to return False if an error occurred while working with the database
        if new_group_token:
            group_id: int = bot_db.get_group_id_by_token(new_group_token)
            if bot_db.add_user_to_db(username, psw_salt, psw_hash, group_id, telegram_id):
                create_table_group(f"budget_{group_id}")
                bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "congratulations")}")
                bot.send_sticker(message.chat.id,f"{Stickers.get_sticker_by_id("id_4")}")
                bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "your")} token:")
                bot.send_message(message.chat.id, new_group_token)
                logger_bot.info(f"New user (new group): ID: {telegram_id}, group: {group_id}")
                reply_menu_buttons_register(message)
            else:
                bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "create_new_user_error")}. "
                                                  f"{get_phrase_by_language(user_language, "contact_support")}")
                logger_bot.error(f"Error adding new user to database: ID: {telegram_id}, username: {username}, "
                                 f"psw salt: {psw_salt}, psw hash: {psw_hash}, group id: {group_id}")
                reply_menu_buttons_not_register(message)
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "create_new_user_error")}. "
                                              f"{get_phrase_by_language(user_language, "contact_support")}")
            logger_bot.error(f"Error adding new user to database: ID: {telegram_id}, username: {username}, "
                             f"psw salt: {psw_salt}, psw hash: {psw_hash}")
            reply_menu_buttons_not_register(message)

    elif len(token) == 32 and token.isalnum() and token.islower():
        group_id: int = bot_db.get_group_id_by_token(token)
        group_not_full: bool = bot_db.check_limit_users_in_group(group_id)
        if group_not_full:  # if the group doesn't exist, group_not_full will be set to False in the try/except
            if bot_db.add_user_to_db(username, psw_salt, psw_hash, group_id, telegram_id):
                bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "congratulations")}")
                bot.send_sticker(message.chat.id,f"{Stickers.get_sticker_by_id("id_4")}")
                logger_bot.info(f"New user: ID: {telegram_id}, group: {group_id}")
                reply_menu_buttons_register(message)
            else:
                bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "create_new_user_error")}. "
                                                  f"{get_phrase_by_language(user_language, "contact_support")}")
                logger_bot.error(f"Error adding new user to database: ID: {telegram_id}, username: {username}, "
                                 f"psw salt: {psw_salt}, psw hash: {psw_hash}, group id: {group_id}")
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "group_is_full")}")
            logger_bot.info(f"Trying to add to a full group: ID: {telegram_id}, group id: {group_id}")

    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "invalid_token_format")}")
        logger_bot.info(f"Authorization attempt with incorrect token format. Token: {token}, ID: {telegram_id}")
        reply_buttons(message)
    close_db(connection)


@timeit
def view_table(message) -> None:
    user_language: str = check_user_language(message)
    telegram_id: int = message.from_user.id
    res: bool = check_user_access(message)
    if res:  # user authorization check
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        # the last entry will be at the bottom of the message <- [::-1] reverses the list
        data: list = bot_db.select_data_for_household_table(int(group_id), 10)[::-1]
        close_db(connection)
        if data:
            bot.send_message(message.chat.id,
                             '\n'.join([f"ID: {item[0]}\n"
                                        f"{get_phrase_by_language(user_language, "total")}: {item[1]}\n"
                                        f"{get_phrase_by_language(user_language, "username")}: {item[2]}\n"
                                        f"{get_phrase_by_language(user_language, "transfer")}: {item[3]}\n"
                                        f"{get_phrase_by_language(user_language, "category")}: {item[4]}\n"
                                        f"{get_phrase_by_language(user_language, "datetime")}: {item[5]}\n"
                                        f"{get_phrase_by_language(user_language, "description")}: {item[6]}\n\n"
                                        for item in data]))
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "table_is_empty")}")


@timeit
def get_csv(message) -> None:
    user_language: str = check_user_language(message)
    telegram_id: int = message.from_user.id
    res: bool = check_user_access(message)
    if res:  # user authorization check
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        file_path: str = f"csv_tables/table_{group_id}.csv"
        table_headers: tuple = ("ID", "TOTAL", "USERNAME", "TRANSFER", "CATEGORY", "DATE_TIME", "DESCRIPTION")
        table_data: tuple = bot_db.select_data_for_household_table(group_id, 0)
        close_db(connection)
        if table_data:
            try:
                create_csv_file(file_path, table_headers, table_data)
                file_size: float = get_file_size_kb(file_path)
                file_checksum: str = get_file_checksum(file_path)
                bot.send_document(message.chat.id, open(f"csv_tables/table_{group_id}.csv", 'rb'),
                                  caption=f"{get_phrase_by_language(user_language, "file_size")}: "
                                          f"{"{:.3f}".format(file_size)} kB\n\n"
                                          f"{get_phrase_by_language(user_language, "hashsum")} "
                                          f"(sha-256): {file_checksum}")
            except FileNotFoundError:
                bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "csv_not_found_error")}.")
                logger_bot.error(f"CSV FileNotFoundError. ID: {telegram_id}, group: {group_id}")
            except PermissionError:
                bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "csv_not_found_error")}.")
                logger_bot.error(f"CSV PermissionError. ID: {telegram_id}, group: {group_id}")
            else:
                logger_bot.info(f"CSV: SUCCESS. ID: {telegram_id}, group: {group_id}. "
                                f"File size: {"{:.3f}".format(file_size)} kB, hashsum: {file_checksum}")
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "table_is_empty")}")


@timeit
def get_group_users(message):
    user_language: str = check_user_language(message)
    telegram_id: int = message.from_user.id
    res: bool = check_user_access(message)
    if res:
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        group_users_list: list = bot_db.get_group_users(group_id)
        group_owner: str = bot_db.get_group_owner_username_by_group_id(group_id)
        close_db(connection)
        group_users_str: str = '\n'.join(f"{user} ({get_phrase_by_language(user_language, "owner")})"
                                         if user == group_owner else f"{user}" for user in group_users_list)
        bot.send_message(message.chat.id, group_users_str)


def change_owner(message):
    user_language: str = check_user_language(message)
    telegram_id: int = message.from_user.id
    res: bool = check_user_access(message)
    if res:
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        group_owner: str = bot_db.get_group_owner_username_by_group_id(group_id)
        username: str = bot_db.get_username_by_telegram_id(telegram_id)
        if group_owner == username:
            group_users_list: list = bot_db.get_group_users(group_id)
            if len(group_users_list) == 1:
                bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "small_group_exception")}")
            else:
                group_users_str: str = '\n'.join(f"{user}" for user in group_users_list if user != group_owner)
                bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "username_new_owner")}:\n{group_users_str}")  # noqa (E501)
                bot.register_next_step_handler(message, process_change_owner, group_id)
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "not_owner_exception")}")
        close_db(connection)


def process_change_owner(message, group_id: int):
    user_language: str = check_user_language(message)
    new_owner: str = message.text
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    telegram_id_new_owner: int = bot_db.get_telegram_id_by_username(new_owner)
    user_is_owner: bool = bot_db.check_username_is_group_owner(new_owner, group_id)
    user_from_current_group: bool = True if bot_db.get_group_id_by_username(new_owner) == group_id else False

    if user_is_owner:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "current_owner_exception")}")
    elif user_from_current_group:
        if bot_db.update_group_owner(telegram_id_new_owner, group_id):
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "owner_has_been_changed")}")
            logger_bot.info(f"Group owner changed: group #{group_id}, new owner: {new_owner}")
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "error_change_owner")}")
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "check_correct_username")}\n"
                                          f"{get_phrase_by_language(user_language, "unknown_user_in_group")}")
    close_db(connection)


def delete_account(message):
    user_language: str = check_user_language(message)
    telegram_id: int = message.from_user.id
    res: bool = check_user_access(message)

    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton(f"👍 {get_phrase_by_language(user_language, "YES")}")
    btn2 = types.KeyboardButton(f"👎 {get_phrase_by_language(user_language, "NO")}")
    markup_1.add(btn1, btn2)
    if res:
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        username: str = bot_db.get_username_by_telegram_id(telegram_id)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        user_is_owner: bool = bot_db.check_username_is_group_owner(username, group_id)
        close_db(connection)

        if user_is_owner:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "owner_try_delete_account")}")
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "confirmation_delete")}",
                             reply_markup=markup_1)
            bot.register_next_step_handler(message, process_delete_account, username)


def process_delete_account(message, username: str):
    user_language: str = check_user_language(message)
    user_choice: str = message.text
    if user_choice == f"👍 {get_phrase_by_language(user_language, "YES")}":
        markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton("Start")
        markup_1.add(btn1)

        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "parting")}")

        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        bot_db.delete_username_from_users(username)
        close_db(connection)

        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "account_is_deleted")}",
                         reply_markup=markup_1)
        logger_bot.info(f"User deleted the account. ID: {message.from_user.id}")

    elif user_choice == f"👎 {get_phrase_by_language(user_language, "NO")}":
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "stay_with_us")}")
        start(message)

    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "unknown_message")}")
        start(message)
        logger_bot.info(f"Unrecognized message when deleting an account. "
                        f"ID: {message.from_user.id}, message: {user_choice}")


def delete_user(message):
    user_language: str = check_user_language(message)
    telegram_id: int = message.from_user.id
    res: bool = check_user_access(message)
    if res:
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        group_owner: str = bot_db.get_group_owner_username_by_group_id(group_id)
        username: str = bot_db.get_username_by_telegram_id(telegram_id)
        user_is_owner: bool = bot_db.check_username_is_group_owner(username, group_id)
        if user_is_owner:
            group_users_list: list = bot_db.get_group_users(group_id)
            if len(group_users_list) == 1:
                bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "exception_one_user_in_group")}\n"  # noqa (E501)
                                                  f"{get_phrase_by_language(user_language, "select_to_delete")}")
            else:
                group_users_str: str = '\n'.join(f"{user}" for user in group_users_list if user != group_owner)
                bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "select_new_owner")}\n"
                                                  f"{group_users_str}")
                bot.register_next_step_handler(message, process_delete_user, group_id, group_users_list)
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "owner_privileges")}")
        close_db(connection)


def process_delete_user(message, group_id: int, group_users_list: list):
    user_language: str = check_user_language(message)
    username_to_delete: str = message.text
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    user_is_owner: bool = bot_db.check_username_is_group_owner(username_to_delete, group_id)

    if user_is_owner:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "current_owner_exception")}")

    elif username_to_delete not in group_users_list:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "check_correct_username")}\n"
                                          f"{get_phrase_by_language(user_language, "unknown_user_in_group")}")
    else:
        if bot_db.delete_username_from_users(username_to_delete):
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "user_removed")}")
            logger_bot.info(f"'{username_to_delete}' deleted by group owner from group #{group_id}")
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "error_user_delete")}")
            logger_bot.warning(f"Error removing '{username_to_delete}' from group #{group_id}")

    close_db(connection)


@timeit
def delete_group(message):
    user_language: str = check_user_language(message)
    markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton(f"🌧️ {get_phrase_by_language(user_language, "YES")}")
    btn2 = types.KeyboardButton(f"🌤️ {get_phrase_by_language(user_language, "NO")}")
    markup_1.add(btn1, btn2)

    telegram_id: int = message.from_user.id
    res: bool = check_user_access(message)
    if res:
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        username: str = bot_db.get_username_by_telegram_id(telegram_id)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        user_is_owner: bool = bot_db.check_username_is_group_owner(username, group_id)
        if user_is_owner:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "are_you_sure")}\n"
                                              f"{get_phrase_by_language(user_language, "delete_table")}", reply_markup=markup_1)  # noqa (E501)
            bot.register_next_step_handler(message, process_delete_group, group_id)
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "not_deleted_by_owner")}")
        close_db(connection)


def process_delete_group(message, group_id: int):
    user_language: str = check_user_language(message)
    user_choice: str = message.text

    if user_choice == f"🌧️ {get_phrase_by_language(user_language, "YES")}":
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "parting")}")

        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        bot_db.delete_group_with_users(group_id)
        close_db(connection)

        markup_1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton("Start")
        markup_1.add(btn1)

        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "remove_completed")}", reply_markup=markup_1)  # noqa (E501)
        logger_bot.info(f"User deleted the group. ID: {message.from_user.id}, group #{group_id}")
    elif user_choice == f"🌤️ {get_phrase_by_language(user_language, "NO")}":
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "stay_with_us")}")
        start(message)
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "unknown_message")}")
        start(message)
        logger_bot.info(f"Unrecognized message when deleting group. "
                        f"ID: {message.from_user.id}, message: {user_choice}, group #{group_id}")


# checking whether the user is registered in the project
# (since he may accidentally end up in a menu that is intended only for registered users)
def user_is_registered(message) -> bool:
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    telegram_id: int = message.from_user.id
    res: bool = bot_db.check_telegram_id_is_exist(telegram_id)
    if res:
        bot_db.update_user_last_login_by_telegram_id(telegram_id)  # update date of the last user activity in database
        close_db(connection)
        return True
    close_db(connection)
    return False


def check_user_access(message) -> bool:
    user_language: str = check_user_language(message)
    telegram_id: int = message.from_user.id
    res: bool = user_is_registered(message)
    if res:
        return True
    bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "not_register")}")
    bot.send_sticker(message.chat.id, f"{Stickers.get_sticker_by_id("id_5")}")
    logger_bot.info(f"Unregistered user interaction. ID: {telegram_id}")
    return False


def check_user_language(message) -> str:
    """
    Makes a request to the database via the get_user_language function.
    The telegram id of the user taken from the message is used.
    """
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    telegram_id: int = message.from_user.id
    language: str = bot_db.get_user_language(telegram_id)
    return language


def get_phrase_by_language(language: str, phrase: str) -> str:
    return Dictionary.receive_translation(language, phrase)


@bot.message_handler(content_types=['text'])
def text(message) -> None:
    user_language: str = check_user_language(message)
    if message.text == "Start":
        start(message)
    elif message.text == f"❓ {get_phrase_by_language(user_language, "help")}":
        help(message)
    elif message.text == f"📎 {get_phrase_by_language(user_language, "link_github")}":
        project_github(message)
    elif message.text == f"💻 {get_phrase_by_language(user_language, "my")} Telegram ID":
        get_my_id(message)
    elif message.text == "🤡 I want to register":
        registration(message)
    elif message.text == f"🔐 {get_phrase_by_language(user_language, "get_my_token")}":
        get_my_token(message)
    elif message.text == f"💵 {get_phrase_by_language(user_language, "table_manage")}":
        res: bool = check_user_access(message)
        if res:
            table_manage_get_buttons(message)
        else:
            reply_menu_buttons_not_register(message)
    elif message.text == f"📖 {get_phrase_by_language(user_language, "view_table")}":
        view_table(message)
    elif message.text == f"📈 {get_phrase_by_language(user_language, "add_income")}":
        add_income(message)
    elif message.text == f"📉 {get_phrase_by_language(user_language, "add_expense")}":
        add_expense(message)
    elif message.text == f"❌ {get_phrase_by_language(user_language, "del_record")}":
        delete_record(message)
    elif message.text == f"🗃️ {get_phrase_by_language(user_language, "get_csv")}":
        get_csv(message)
    elif message.text == f"💻 {get_phrase_by_language(user_language, "group_settings")}":
        res: bool = check_user_access(message)
        if res:
            group_settings_get_buttons(message)
        else:
            reply_menu_buttons_not_register(message)
    elif message.text == f"⭐ {get_phrase_by_language(user_language, "premium")}":
        premium(message)
    elif message.text == f"🌍 {get_phrase_by_language(user_language, "group_users")}":
        get_group_users(message)
    elif message.text == f"🗑️ {get_phrase_by_language(user_language, "delete_account")}":
        delete_account(message)
    elif message.text == f"🚫 {get_phrase_by_language(user_language, "delete_group")}":
        delete_group(message)
    elif message.text == f"🔑 {get_phrase_by_language(user_language, "change_owner")}":
        change_owner(message)
    elif message.text == f"🤖 {get_phrase_by_language(user_language, "delete_user")}":
        delete_user(message)
    elif (message.text == f"↩️ {get_phrase_by_language(user_language, "back")}" or
          message.text == f"↩️ {get_phrase_by_language(user_language, "back_to_menu")}"):
        reply_buttons(message)
    elif message.text == f"{get_phrase_by_language(user_language, "change_language")}":
        change_language(message)
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "misunderstanding")} :(")


bot.polling(none_stop=True)
