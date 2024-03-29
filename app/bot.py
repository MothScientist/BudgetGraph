""" Setting up a bot via BotFather
Name: At your discretion

About: At your discretion

Description: At your discretion

Description Picture: At your discretion

Bot Picture: At your discretion

Commands:
start - Start
help - Help
project_github - GitHub
change_language - Change language
get_my_id - Get my Telegram ID
premium - Premium
"""

from os import getenv
import asyncio
from datetime import datetime, UTC
from dotenv import load_dotenv
from secrets import compare_digest
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import sys

sys.path.append('../')

from app.db_manager import DatabaseQueries, connect_db, close_db  # noqa

from app.encryption import getting_hash, get_salt  # noqa

from app.validation import (date_validation, value_validation, description_validation,
                            username_validation, password_validation, category_validation)  # noqa

from app.create_csv import create_csv_file, get_file_size_kb, get_file_checksum  # noqa

from app.dictionary import Dictionary, Stickers  # noqa
from app.time_checking import timeit  # noqa
from app.logger import setup_logger  # noqa


load_dotenv()  # Load environment variables from .env file

bot_token = getenv("BOT_TOKEN")  # Get the bot token from an environment variable
bot = telebot.TeleBot(bot_token, skip_pending=True)  # type: ignore

logger_bot = setup_logger("logs/BotLog.log", "bot_logger")


@timeit
def reply_menu_buttons_register(message):
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton(f"💵 {get_phrase_by_language(user_language, "table_manage")}")
    btn2 = KeyboardButton(f"💻 {get_phrase_by_language(user_language, "group_settings")}")
    btn3 = KeyboardButton(f"🔐 {get_phrase_by_language(user_language, "get_my_token")}")
    btn4 = KeyboardButton(f"⭐ {get_phrase_by_language(user_language, "premium")}")
    markup_1.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id,
                     f"{get_phrase_by_language(user_language, "click_need_button")} :)",
                     reply_markup=markup_1)


@timeit
def reply_menu_buttons_not_register(message):
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton("🤡 I want to register")
    btn2 = KeyboardButton(f"⭐ {get_phrase_by_language(user_language, "premium")}")
    markup_1.add(btn1, btn2)

    bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "click_need_button")} :)",
                     reply_markup=markup_1)


@timeit
def table_manage_get_buttons(message):
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton(f"📖 {get_phrase_by_language(user_language, "view_table")}")
    btn2 = KeyboardButton(f"📈 {get_phrase_by_language(user_language, "add_income")}")
    btn3 = KeyboardButton(f"📉 {get_phrase_by_language(user_language, "add_expense")}")
    btn4 = KeyboardButton(f"❌ {get_phrase_by_language(user_language, "del_record")}")
    btn5 = KeyboardButton(f"🗃️ {get_phrase_by_language(user_language, "get_csv")}")
    btn6 = KeyboardButton(f"↩️ {get_phrase_by_language(user_language, "back")}")
    markup_1.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "click_need_button")} "
                                      f"({get_phrase_by_language(user_language, "table_manage")})",
                     reply_markup=markup_1)


@timeit
def group_settings_get_buttons(message):
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton(f"🌍 {get_phrase_by_language(user_language, "group_users")}")
    btn2 = KeyboardButton(f"🗑️ {get_phrase_by_language(user_language, "delete_account")}")
    btn3 = KeyboardButton(f"🚫 {get_phrase_by_language(user_language, "delete_group")}")
    btn4 = KeyboardButton(f"🔑 {get_phrase_by_language(user_language, "change_owner")}")
    btn5 = KeyboardButton(f"🤖 {get_phrase_by_language(user_language, "delete_user")}")
    btn6 = KeyboardButton(f"↩️ {get_phrase_by_language(user_language, "back")}")
    markup_1.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "click_need_button")} "
                                      f"({get_phrase_by_language(user_language, "group_settings")})",
                     reply_markup=markup_1)


@timeit
def reply_buttons(message):
    telegram_id: int = message.from_user.id
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    res: str = bot_db.get_username_by_telegram_id(telegram_id)
    close_db(connection)
    if res:
        reply_menu_buttons_register(message)
    else:
        reply_menu_buttons_not_register(message)


@bot.message_handler(commands=['start'])
def start(message) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    res: bool = user_is_registered(telegram_id)
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
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    bot.send_message(message.chat.id, get_phrase_by_language(user_language, "support_information"))


@bot.message_handler(commands=['get_my_id'])
def get_my_id(message) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    bot.send_sticker(message.chat.id,Stickers.get_sticker_by_id("id_3"))
    bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "your")} "
                                      f"telegram ID: {message.from_user.id}")


@bot.message_handler(commands=['project_github'])
def project_github(message) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("github.com", url="https://github.com/MothScientist/BudgetGraph"))
    bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "project_on_github")}:",
                     reply_markup=markup)


@bot.message_handler(commands=['premium'])
def premium(message):
    bot.send_message(message.chat.id, "soon")


@bot.message_handler(commands=['change_language'])
def change_language(message) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    markup_1 = InlineKeyboardMarkup(row_width=2)
    # button_labels: tuple = ("English", "Español", "Русский", "Français", "Deutsch", "Islenskur")

    markup_1.add(InlineKeyboardButton("English", callback_data="change_language_en"))
    markup_1.add(InlineKeyboardButton("Español", callback_data="change_language_es"))
    markup_1.add(InlineKeyboardButton("Русский", callback_data="change_language_ru"))
    markup_1.add(InlineKeyboardButton("Français", callback_data="change_language_fr"))
    markup_1.add(InlineKeyboardButton("Deutsch", callback_data="change_language_de"))
    markup_1.add(InlineKeyboardButton("Islenskur", callback_data="change_language_is"))

    bot.send_message(message.chat.id,f"{get_phrase_by_language(user_language, "choose_language")}:",
                     reply_markup=markup_1)

# TODO - remove the inlinekeyboard after pressing


@bot.callback_query_handler(func=lambda call: call.data.startswith('change_language'))
def callback_query_change_language(call):
    telegram_id: int = call.from_user.id
    user_language: str = check_user_language(telegram_id)
    new_user_language: str = call.data[-2:]
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    res: bool = bot_db.add_user_language(telegram_id, new_user_language)
    close_db(connection)
    if res:
        user_language: str = check_user_language(telegram_id)  # changing the user's language to a new option
        bot.answer_callback_query(call.id,
                                  f"{get_phrase_by_language(user_language, "great")}\n"
                                  f"{get_phrase_by_language(user_language, "language_changed")}")
        logger_bot.info(f"Successful language change. Telegram ID: {telegram_id}, language: {new_user_language}")
        restart_language_after_changes(call)  # Reload button names and text for new language
    else:
        bot.answer_callback_query(call.id,
                                  f"{get_phrase_by_language(user_language, "error_change_language")}.\n"
                                  f"{get_phrase_by_language(user_language, "contact_support")}")
        logger_bot.error(f"Error language change. Telegram ID: {telegram_id}, language: {new_user_language}")


def restart_language_after_changes(call) -> None:
    """
    Since the start command is called with the message parameter,
    and this object cannot be obtained from the callback function,
    then this function was made as a reboot of the buttons after changing the language.
    """
    telegram_id: int = call.from_user.id
    user_language: str = check_user_language(telegram_id)
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup_1.add(KeyboardButton("/start"))
    # Для корректной смены языка, пожалуйста, перезагрузите бота, нажав на кнопку /start. Ваши данные не пострадают!
    bot.send_message(call.message.chat.id,
                     f"{get_phrase_by_language(user_language, "start_after_change_language")}\n"
                     f"{get_phrase_by_language(user_language, "data_is_safe")}",
                     reply_markup=markup_1)


def get_my_token(message) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    token: str = bot_db.get_token_by_telegram_id(telegram_id)
    close_db(connection)
    token: str = token if token else get_phrase_by_language(user_language, "unknown")
    bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "group_token")}:")
    bot.send_message(message.chat.id, token)


def add_income(message) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    res: bool = check_user_access(message)
    if res:  # user authorization check
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "enter_income")}:")
        bot.register_next_step_handler(message, process_add_date_for_transfer, False)


def add_expense(message):
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    res: bool = check_user_access(message)
    if res:  # user authorization check
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "enter_expense")}:")
        bot.register_next_step_handler(message, process_add_date_for_transfer, True)


def process_add_date_for_transfer(message, is_negative: bool) -> None:
    """
    Adds income and expense to the database.
    Accepts an unvalidated value,
    performs validation and enters it into the database.
    
    Args:
        message:
        is_negative (bool): False if X > 0 (add_income), True if X < 0 (add_expense)
        X = 0 - will be rejected by the validator

    Returns: None
    """
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    value: str = message.text
    value: int = value_validation(value)
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    today_date: str = datetime.now(UTC).strftime('%d/%m/%Y')
    btn1 = KeyboardButton(today_date)
    markup_1.add(btn1)

    if value:
        value *= -1 if is_negative else 1
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "set_date")} (DD/MM/YYYY)",
                         reply_markup=markup_1)
        bot.register_next_step_handler(message, process_add_category_for_transfer, value)
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "invalid_value")}")


def process_add_category_for_transfer(message, value: int) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    button_labels: tuple = (
        get_phrase_by_language(user_language, "supermarkets"),
        get_phrase_by_language(user_language, "restaurants"),
        get_phrase_by_language(user_language, "clothes"),
        get_phrase_by_language(user_language, "medicine"),
        get_phrase_by_language(user_language, "transport"),
        get_phrase_by_language(user_language, "devices"),
        get_phrase_by_language(user_language, "education"),
        get_phrase_by_language(user_language, "services"),
        get_phrase_by_language(user_language, "travel"),
        get_phrase_by_language(user_language, "housing"),
        get_phrase_by_language(user_language, "transfer"),
        get_phrase_by_language(user_language, "investments"),
        get_phrase_by_language(user_language, "hobby"),
        get_phrase_by_language(user_language, "jewelry"),
        get_phrase_by_language(user_language, "salary"),
        get_phrase_by_language(user_language, "charity"),
        get_phrase_by_language(user_language, "other")
    )
    buttons: list = [KeyboardButton(label) for label in button_labels]  # Assembling buttons from the tuple above
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
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    btn1 = KeyboardButton(get_phrase_by_language(user_language, "no_description"))
    markup_1.add(btn1)
    category: str = message.text
    category_is_valid: bool = category_validation(user_language, category)

    if category_is_valid:
        bot.send_message(message.chat.id, get_phrase_by_language(user_language, "add_description"), reply_markup=markup_1)  # noqa (E501)
        bot.register_next_step_handler(message, process_transfer_final, value, record_date, category)
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "invalid_category")}")  # noqa (E501)
        reply_buttons(message)
        logger_bot.info(f"User entered an incorrect category. Category: {category}")


def process_transfer_final(message, value: int, record_date: str, category: str) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    description: str = message.text
    description_is_valid: bool = description_validation(description)

    if description == get_phrase_by_language(user_language, "no_description"):
        description: str = ""

    if description_is_valid:
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        username: str = bot_db.get_username_by_telegram_id(telegram_id)
        if bot_db.add_transaction_to_db(username, value, record_date, category, description):
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "entry_add_success")}!")
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "entry_add_error")}\n"
                                              f"{get_phrase_by_language(user_language, "contact_support")}")
        close_db(connection)
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "invalid_value")}")
    table_manage_get_buttons(message)


def delete_record(message) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    res: bool = check_user_access(message)
    if res:  # user authorization check
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "entry_record_id")}:")
        bot.register_next_step_handler(message, process_delete_record)


def process_delete_record(message):
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = KeyboardButton(f"❌ {get_phrase_by_language(user_language, "del_record")}")
    btn2 = KeyboardButton(f"↩️ {get_phrase_by_language(user_language, "back_to_menu")}")
    markup_1.add(btn1, btn2)
    transaction_id: str = message.text
    transaction_id: int = value_validation(transaction_id)

    if transaction_id:
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        if group_id and bot_db.check_record_id_is_exist(group_id, transaction_id):
            bot_db.process_delete_transaction_record(group_id, transaction_id)
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "success")}!")
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "enry_record_id_error")}", reply_markup=markup_1)  # noqa (E501)
        close_db(connection)
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "invalid_value")}", reply_markup=markup_1)  # noqa (E501)


def registration(message) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    res: str = bot_db.get_username_by_telegram_id(telegram_id)
    close_db(connection)
    if not res:  # Checking whether the user is already registered and accidentally ended up in this menu.
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "enter_username")}:")
        bot.register_next_step_handler(message, process_username)
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "already_registered")}!")
        reply_buttons(message)


def process_username(message):
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    username: str = message.text
    if asyncio.run(username_validation(username)):
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "enter_password")}:")
        bot.register_next_step_handler(message, process_psw, username)
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "invalid_username")}")


def process_psw(message, username: str):
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton("None")
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
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton("None")
    markup_1.add(btn1)

    token: str = message.text
    connection = connect_db()
    bot_db = DatabaseQueries(connection)

    if compare_digest(token, "None"):  # noqa (PW100) - I don’t think there is any need for time attack protection here
        new_group_token: str = bot_db.create_new_group(telegram_id)
        # There is a chance to return False if an error occurred while working with the database
        if new_group_token:
            group_id: int = bot_db.get_group_id_by_token(new_group_token)
            if bot_db.add_user_to_db(username, psw_salt, psw_hash, group_id, telegram_id):
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
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    res: bool = check_user_access(message)
    if res:  # user authorization check
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        # the last entry should be at the bottom of the message -> [::-1] reverse list
        data: list = bot_db.select_data_for_household_table(group_id, 10)[::-1]
        close_db(connection)
        if data:
            # Generating a single message from nested lists of the 'data' list
            bot.send_message(message.chat.id,
                             '\n'.join([f"ID: {table_entry[0]}\n"
                                        f"{get_phrase_by_language(user_language, "username")}: {table_entry[1]}\n"
                                        f"{get_phrase_by_language(user_language, "transfer")}: {table_entry[2]}\n"
                                        f"{get_phrase_by_language(user_language, "total")}: {table_entry[3]}\n"
                                        f"{get_phrase_by_language(user_language, "datetime")}: {table_entry[4]}\n"
                                        f"{get_phrase_by_language(user_language, "category")}: {table_entry[5]}\n"
                                        f"{get_phrase_by_language(user_language, "description")}: {table_entry[6]}\n\n"
                                        for table_entry in data]))
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "table_is_empty")}")


@timeit
def get_csv(message) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    res: bool = check_user_access(message)
    if res:  # user authorization check
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        file_path: str = f"csv_tables/table_{group_id}.csv"
        table_headers: tuple = ("ID", "USERNAME", "TRANSFER", "TOTAL", "DATE", "CATEGORY", "DESCRIPTION")
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
            except PermissionError:  # TODO what catches this exception?
                bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "csv_not_found_error")}.")
                logger_bot.error(f"CSV PermissionError. ID: {telegram_id}, group: {group_id}")
            else:
                logger_bot.info(f"CSV: SUCCESS. ID: {telegram_id}, group: {group_id}. "
                                f"File size: {"{:.3f}".format(file_size)} kB, hashsum: {file_checksum}")
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "table_is_empty")}")


@timeit
def get_group_users(message):
    """
    Returns a list of users.

    Example of string generation result:
        Emma
        Olivia (owner)
        Evelyn
        Sophia
        Ava
    """
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    res: bool = check_user_access(message)
    if res:  # user authorization check
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        group_owner_username: str = bot_db.get_group_owner_username_by_group_id(group_id)
        group_users_list: tuple = bot_db.get_group_users(group_id)
        close_db(connection)
        group_users_str: str = '\n'.join(f"{user} ({get_phrase_by_language(user_language, "owner")})"
                                         if user == group_owner_username else f"{user}" for user in group_users_list)
        bot.send_message(message.chat.id, group_users_str)


def change_owner(message):
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    res: bool = check_user_access(message)
    if res:  # user authorization check
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        group_owner_username: str = bot_db.get_group_owner_username_by_group_id(group_id)
        username: str = bot_db.get_username_by_telegram_id(telegram_id)
        if compare_digest(group_owner_username, username):
            group_users_list: tuple = bot_db.get_group_users(group_id)
            if len(group_users_list) == 1:  # If there are no users in the group except the owner
                bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "small_group_exception")}")
            else:
                # List of users as a string without group owner
                group_users_str_without_owner: str = '\n'.join(f"{user}" for user in group_users_list if user != group_owner_username)  # noqa
                bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "username_new_owner")}:\n"
                                                  f"{group_users_str_without_owner}")  # noqa (E501)
                bot.register_next_step_handler(message, process_change_owner, group_id)
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "not_owner_exception")}")
        close_db(connection)


def process_change_owner(message, group_id: int) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)

    new_owner: str = message.text

    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    telegram_id_new_owner: int = bot_db.get_telegram_id_by_username(new_owner)
    user_from_current_group: bool = True if bot_db.get_group_id_by_telegram_id(telegram_id_new_owner) == group_id else False  # noqa
    user_is_owner: bool = bot_db.check_user_is_group_owner_by_telegram_id(telegram_id_new_owner, group_id)

    if user_is_owner:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "current_owner_exception")}")
    elif user_from_current_group:
        if bot_db.update_group_owner(telegram_id_new_owner, group_id):
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "owner_has_been_changed")}")
            logger_bot.info(f"Group owner changed: group #{group_id}, new owner: {new_owner}")
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "error_change_owner")}")
            logger_bot.error(f"Owner change error. Current owner: {telegram_id}, desired owner: {telegram_id_new_owner} "
                             f"- this user is a member of the group.")
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "check_correct_username")}\n"
                                          f"{get_phrase_by_language(user_language, "unknown_user_in_group")}")
        logger_bot.error(f"Owner change error. Current owner: {telegram_id}, desired owner: {new_owner} "
                         f"- this user is not a member of the group.")
    close_db(connection)
    group_settings_get_buttons(message)


def delete_account(message):
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    res: bool = check_user_access(message)

    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton(f"👍 {get_phrase_by_language(user_language, "YES")}")
    btn2 = KeyboardButton(f"👎 {get_phrase_by_language(user_language, "NO")}")
    markup_1.add(btn1, btn2)
    if res:
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        username: str = bot_db.get_username_by_telegram_id(telegram_id)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        user_is_owner: bool = bot_db.check_user_is_group_owner_by_telegram_id(telegram_id, group_id)
        close_db(connection)

        if user_is_owner:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "owner_try_delete_account")}")
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "confirmation_delete")}",
                             reply_markup=markup_1)
            bot.register_next_step_handler(message, process_delete_account, username)


def process_delete_account(message, username: str):
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = KeyboardButton("/start")
    markup_1.add(btn1)
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    user_choice: str = message.text
    if user_choice == f"👍 {get_phrase_by_language(user_language, "YES")}":
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        bot_db.delete_username_from_users(username)
        close_db(connection)
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "parting")}")
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "account_is_deleted")}",
                         reply_markup=markup_1)
        logger_bot.info(f"User deleted the account. ID: {message.from_user.id}")
        start(message)

    elif user_choice == f"👎 {get_phrase_by_language(user_language, "NO")}":
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "stay_with_us")}")
        group_settings_get_buttons(message)

    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "unknown_message")}")
        logger_bot.info(f"Unrecognized message when deleting an account. "
                        f"ID: {message.from_user.id}, message: {user_choice}")
        group_settings_get_buttons(message)


def delete_user(message):
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    res: bool = check_user_access(message)
    if res:
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        group_owner: str = bot_db.get_group_owner_username_by_group_id(group_id)
        user_is_owner: bool = bot_db.check_user_is_group_owner_by_telegram_id(telegram_id, group_id)
        if user_is_owner:
            group_users_list: tuple = bot_db.get_group_users(group_id)
            if len(group_users_list) == 1:  # If there are no users in the group except the owner
                bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "exception_one_user_in_group")}\n"  # noqa (E501)
                                                  f"{get_phrase_by_language(user_language, "select_to_delete")}")
            else:
                # List of users as a string without group owner
                group_users_str_without_owner: str = '\n'.join(f"{user}" for user in group_users_list if user != group_owner)  # noqa
                bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "select_new_owner")}\n"
                                                  f"{group_users_str_without_owner}")
                bot.register_next_step_handler(message, process_delete_user, group_id, group_users_list)
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "owner_privileges")}")
        close_db(connection)


def process_delete_user(message, group_id: int, group_users_list: tuple) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    username_user_to_delete: str = message.text
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    telegram_id_user_to_delete: int = bot_db.get_telegram_id_by_username(username_user_to_delete)
    user_to_delete_is_owner: bool = bot_db.check_user_is_group_owner_by_telegram_id(telegram_id_user_to_delete, group_id)  # noqa(E501)

    if user_to_delete_is_owner:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "current_owner_exception")}")

    elif username_user_to_delete not in group_users_list:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "check_correct_username")}\n"
                                          f"{get_phrase_by_language(user_language, "unknown_user_in_group")}")
    else:
        if bot_db.delete_username_from_users_by_telegram_id(telegram_id_user_to_delete):
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "user_removed")}")
            logger_bot.info(f"'{username_user_to_delete}' deleted by group owner from group #{group_id}")
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "error_user_delete")}")
            logger_bot.warning(f"Error removing '{username_user_to_delete}' from group #{group_id}")

    close_db(connection)
    group_settings_get_buttons(message)


@timeit
def delete_group(message) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton(f"🌧️ {get_phrase_by_language(user_language, "YES")}")
    btn2 = KeyboardButton(f"🌤️ {get_phrase_by_language(user_language, "NO")}")
    markup_1.add(btn1, btn2)

    res: bool = check_user_access(message)
    if res:
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
        user_is_owner: bool = bot_db.check_user_is_group_owner_by_telegram_id(telegram_id, group_id)

        if user_is_owner:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "are_you_sure")}\n"
                                              f"{get_phrase_by_language(user_language, "delete_table")}", reply_markup=markup_1)  # noqa (E501)
            bot.register_next_step_handler(message, process_delete_group, group_id)
        else:
            bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "not_deleted_by_owner")}")

        close_db(connection)


def process_delete_group(message, group_id: int) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    user_choice: str = message.text

    if user_choice == f"🌧️ {get_phrase_by_language(user_language, "YES")}":
        connection = connect_db()
        bot_db = DatabaseQueries(connection)
        bot_db.delete_group_with_users(group_id)
        close_db(connection)
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "parting")}")
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "remove_completed")}")
        logger_bot.info(f"User deleted the group. ID: {message.from_user.id}, group #{group_id}")
        start(message)
    elif user_choice == f"🌤️ {get_phrase_by_language(user_language, "NO")}":
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "stay_with_us")}")
        group_settings_get_buttons(message)
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "unknown_message")}")
        logger_bot.info(f"Unrecognized message when deleting group. "
                        f"ID: {message.from_user.id}, message: {user_choice}, group #{group_id}")
        group_settings_get_buttons(message)


# TODO reuse func
def get_str_with_group_users(telegram_id: int, with_owner: bool) -> str:
    user_language: str = check_user_language(telegram_id)
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    group_id: int = bot_db.get_group_id_by_telegram_id(telegram_id)
    group_owner_username: str = bot_db.get_group_owner_username_by_group_id(group_id)
    group_users_list: tuple = bot_db.get_group_users(group_id)

    if with_owner:
        res: str = '\n'.join(f"{user} ({get_phrase_by_language(user_language, "owner")})"
                                         if user == group_owner_username else f"{user}" for user in group_users_list)
    else:
        res: str = '\n'.join(f"{user}" for user in group_users_list if user != group_owner_username)

    close_db(connection)
    return res


def user_is_registered(telegram_id: int) -> bool:
    """
    We check whether the user is registered in the project.
    Since the user may accidentally end up in a menu intended only for registered users.
    """
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    res: bool = bot_db.check_telegram_id_is_exist(telegram_id)
    if res:
        bot_db.update_user_last_login_by_telegram_id(telegram_id)  # update date of the last user activity in database
    close_db(connection)
    if res:  # To avoid duplicating the function of closing the connection to the database.
        return True
    return False


def check_user_access(message) -> bool:
    """
    Automatic verification of user registration.
    The user does not need to manually enter a login and password.

    This check is called with each user action to avoid actions after removing the user from the group
    and to suggest relevant buttons and functions.
    """
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    res: bool = user_is_registered(telegram_id)
    if res:
        return True
    bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "not_register")}")
    bot.send_sticker(message.chat.id, f"{Stickers.get_sticker_by_id("id_5")}")
    logger_bot.info(f"Unregistered user interaction. ID: {telegram_id}")
    return False


def check_user_language(telegram_id: int) -> str:
    """
    Makes a request to the database via the get_user_language function.
    The telegram id of the user taken from the message is used.
    """
    connection = connect_db()
    bot_db = DatabaseQueries(connection)
    language: str = bot_db.get_user_language(telegram_id)
    close_db(connection)
    return language


def get_phrase_by_language(language: str, phrase: str) -> str:
    return Dictionary.receive_translation(language, phrase)


@bot.message_handler(content_types=['text'])
def text(message) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    if message.text == "🤡 I want to register":
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
    else:
        bot.send_message(message.chat.id, f"{get_phrase_by_language(user_language, "misunderstanding")} :(")


bot.polling(none_stop=True)
