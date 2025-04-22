"""
The module responsible for setting up, launching and operating the bot
"""

from sys import path as sys_path
from asyncio import run as asyncio_run
from os import getenv, path
from secrets import compare_digest
from datetime import datetime, UTC
from dotenv import load_dotenv
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

sys_path.append('../')
from budget_graph.logger import setup_logger
from budget_graph.global_config import GlobalConfig
from budget_graph.registration_service import user_registration
from budget_graph.dictionary import Stickers, receive_translation
from budget_graph.encryption import getting_hash, get_salt, logging_hash
from budget_graph.create_csv import CsvFileWithTable, check_csv_is_actual
from budget_graph.user_cache_structure import UserLanguageCache, UserRegistrationStatusCache
from budget_graph.db_manager import connect_defer_close_db
from budget_graph.validation import date_validation, value_validation, description_validation, username_validation, \
    password_validation, category_validation
from budget_graph.helpers import StorageMsgIdForDeleteAfterOperation, get_category_button_labels, get_bot_commands, \
    get_category_translate, get_timezone_buttons, get_language_buttons


load_dotenv()  # Load environment variables from .env file

bot_token = getenv('BOT_TOKEN')  # Get the bot token from an environment variable
bot = TeleBot(bot_token, skip_pending=True)

logger_bot = setup_logger('logs/BotLog.log', 'bot_logger')

GlobalConfig.set_config()

# change the list of the bot’s commands --------------------------------------------------------------------------------
bot.set_my_commands(get_bot_commands())
# change the bot’s description, which is shown in the chat with the bot if the chat is empty
# bot.set_my_description('Get started with the easy budgeting bot by entering the /start command')
# change the bot’s name
# bot.set_my_name('BudgetGraph')
# change the bot’s short description, which is shown on the bot’s profile page
# bot.set_my_short_description('Simple and fast budget control') -------------------------------------------------------


def reply_menu_buttons_register(message):
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton(f"💵 {receive_translation(user_language, 'table_manage')}")
    btn2 = KeyboardButton(f"💻 {receive_translation(user_language, 'group_settings')}")
    btn3 = KeyboardButton(f"🔐 {receive_translation(user_language, 'get_my_token')}")
    btn4 = KeyboardButton(f"⭐ {receive_translation(user_language, 'premium')}")
    markup_1.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, receive_translation(user_language, "click_need_button"), reply_markup=markup_1)


def reply_menu_buttons_not_register(message):
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton(f"📬 {receive_translation(user_language, 'register')}")
    btn2 = KeyboardButton(f"⭐ {receive_translation(user_language, 'premium')}")
    markup_1.add(btn1, btn2)

    bot.send_message(message.chat.id, receive_translation(user_language, 'click_need_button'), reply_markup=markup_1)


def table_manage_get_buttons(message):
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton(f"📖 {receive_translation(user_language, "view_table")}")
    btn2 = KeyboardButton(f"📈 {receive_translation(user_language, "add_income")}")
    btn3 = KeyboardButton(f"📉 {receive_translation(user_language, "add_expense")}")
    btn4 = KeyboardButton(f"❌ {receive_translation(user_language, "del_record")}")
    btn5 = KeyboardButton(f"🗃️ {receive_translation(user_language, "get_csv")}")
    btn6 = KeyboardButton(f"↩️ {receive_translation(user_language, "back")}")
    markup_1.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, f"{receive_translation(user_language, "click_need_button")} "
                                      f"({receive_translation(user_language, "table_manage")})",
                     reply_markup=markup_1)


def group_settings_get_buttons(message):
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton(f"🌍 {receive_translation(user_language, "group_users")}")
    btn2 = KeyboardButton(f"🗑️ {receive_translation(user_language, "delete_account")}")
    btn3 = KeyboardButton(f"🚫 {receive_translation(user_language, "delete_group")}")
    btn4 = KeyboardButton(f"🔑 {receive_translation(user_language, "change_owner")}")
    btn5 = KeyboardButton(f"🤖 {receive_translation(user_language, "delete_user")}")
    btn6 = KeyboardButton(f"↩️ {receive_translation(user_language, "back")}")
    markup_1.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id,
                     f"{receive_translation(user_language, "click_need_button")} "
                     f"({receive_translation(user_language, "group_settings")})",
                     reply_markup=markup_1)


@connect_defer_close_db
def reply_buttons(db_connection, message):
    if db_connection.get_username_by_telegram_id(message.from_user.id):
        reply_menu_buttons_register(message)
    else:
        reply_menu_buttons_not_register(message)


@bot.message_handler(commands=['start'])
def start(message) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)

    if user_is_registered(telegram_id):
        # to send a sticker in .webp format no larger than 512x512 pixel
        # sticker = open("H:\telebot\stickers\stick_name.webp", "rb")
        # bot.send_sticker(message.chat.id, sticker)
        bot.send_message(message.chat.id,
                         f"{receive_translation(user_language, "greetings")}"
                         f" {message.from_user.first_name}!\n"
                         f"{receive_translation(user_language, "our_user")}")
        bot.send_sticker(message.chat.id,
                         f"{Stickers.get_sticker_by_id("id_1")}")
        reply_menu_buttons_register(message)
        logger_bot.info(f"Bot start with registration: "
                        f"TelegramId={logging_hash(telegram_id)}")
    else:
        bot.send_message(message.chat.id,
                         f"{receive_translation(user_language, "greetings")}"
                         f" {message.from_user.first_name}!\n"
                         f"{receive_translation(user_language, "unknown_user")}")
        bot.send_sticker(message.chat.id,
                         f"{Stickers.get_sticker_by_id("id_2")}")
        reply_menu_buttons_not_register(message)
        logger_bot.info(f"Bot start without registration: "
                        f"TelegramId={logging_hash(telegram_id)}")


@bot.message_handler(commands=['help'])
def help_msg(message) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    bot.send_message(message.chat.id, receive_translation(user_language, 'support_information'))


@bot.message_handler(commands=['get_my_id'])
def get_my_id(message) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    bot.send_sticker(message.chat.id,Stickers.get_sticker_by_id('id_3'))
    bot.send_message(message.chat.id, f"{receive_translation(user_language, "your")} "
                                      f"telegram ID: {message.from_user.id}")


@bot.message_handler(commands=['del_msg_transaction'])
@connect_defer_close_db
def del_msg_transaction(db_connection, message) -> None:
    telegram_id: int = message.from_user.id
    chat_id: int = message.chat.id
    user_language: str = check_user_language(telegram_id)

    if not user_is_registered(telegram_id):
        get_answer_for_unregistered_user(message, telegram_id, user_language, 'del_msg_transaction')
        return

    old_feature_status: bool = db_connection.get_feature_status_del_msg_after_transaction(telegram_id)
    res: bool = db_connection.change_feature_status_del_msg_after_transaction(telegram_id)
    if res and old_feature_status:  # the functionality was enabled
        bot.send_message(chat_id, receive_translation(user_language, 'del_msg_transaction_of'))
    elif res and not old_feature_status:  # the functionality was disabled
        bot.send_message(chat_id, receive_translation(user_language, 'del_msg_transaction_on'))
    else:
        bot.send_message(chat_id, f"{receive_translation(user_language, 'del_msg_transaction_on')}\n"
                                  f"{receive_translation(user_language, 'contact_support')}")


@bot.message_handler(commands=['project_github'])
def project_github(message) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('github.com', url='https://github.com/MothScientist/BudgetGraph'))
    bot.send_message(message.chat.id, f"{receive_translation(user_language, "project_on_github")}:",
                     reply_markup=markup)


@bot.message_handler(commands=['premium'])
def premium(message, user_language: str):
    bot.send_message(message.chat.id, 'soon')
    # TODO - пока идея, что для премиума доступна аналитика по расходам их собственным
    # TODO - если премиум имеет владелец группы, то для всех в группе доступна общая аналитика, но не собственная


@bot.message_handler(commands=['change_timezone'])
def change_timezone(message) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)

    if not user_is_registered(telegram_id):
        get_answer_for_unregistered_user(message, telegram_id, user_language, 'del_msg_transaction')
        return

    bot.send_message(message.chat.id, f"{receive_translation(user_language, 'select_timezone')}:",
                     reply_markup=InlineKeyboardMarkup(get_timezone_buttons()))


@bot.callback_query_handler(func=lambda call: call.data.startswith('change_timezone'))
@connect_defer_close_db
def callback_query_change_timezone(db_connection, call):
    telegram_id: int = call.from_user.id
    user_language: str = check_user_language(telegram_id)
    timezone: int = int(call.data.replace('change_timezone_', '', 1).strip())

    res_query: bool = db_connection.add_user_timezone(telegram_id, timezone)
    if res_query:
        bot.answer_callback_query(call.id,
                                  f"{receive_translation(user_language, "great")}\n"
                                  f"{receive_translation(user_language, "timezone_changed")}")
        logger_bot.info(f"[change_timezone] Successful timezone change. "
                        f"TelegramID: {logging_hash(telegram_id)}, "
                        f"timezone: {timezone}")
    else:
        bot.answer_callback_query(call.id,
                                  f"{receive_translation(user_language, "error_select_timezone")}.\n"
                                  f"{receive_translation(user_language, "contact_support")}")
        logger_bot.error(f"[change_timezone] Error timezone change. "
                         f"TelegramID: {logging_hash(telegram_id)}, "
                         f"timezone: {timezone}")

    bot.delete_message(call.message.chat.id, call.message.message_id)  # delete message with list of languages


@bot.message_handler(commands=['change_language'])
def change_language(message) -> None:
    if GlobalConfig.localization_enable:
        telegram_id: int = message.from_user.id
        user_language: str = check_user_language(telegram_id)
        markup_1 = InlineKeyboardMarkup(get_language_buttons())
        bot.send_message(message.chat.id, f"{receive_translation(user_language, 'choose_language')}:",
                         reply_markup=markup_1)


@bot.callback_query_handler(func=lambda call: call.data.startswith('change_language'))
@connect_defer_close_db
def callback_query_change_language(db_connection, call):
    telegram_id: int = call.from_user.id
    user_language: str = check_user_language(telegram_id)
    # remove old language values from cache
    UserLanguageCache.delete_data_from_cache(telegram_id)
    new_user_language: str = call.data[-2:]

    if db_connection.add_user_language(telegram_id, new_user_language):
        # new value will be written to the cache
        user_language: str = check_user_language(telegram_id)  # change user language to new language
        bot.answer_callback_query(call.id,
                                  f"{receive_translation(user_language, "great")}\n"
                                  f"{receive_translation(user_language, "language_changed")}")
        logger_bot.info(f"[change_language] Successful language change. "
                        f"TelegramID: {logging_hash(telegram_id)}, "
                        f"language: {new_user_language}")
        restart_language_after_changes(call)  # reload button names and text for new language
    else:
        bot.answer_callback_query(call.id,
                                  f"{receive_translation(user_language, "error_change_language")}.\n"
                                  f"{receive_translation(user_language, "contact_support")}")
        logger_bot.error(f"[change_language] Error language change. "
                         f"TelegramID: {logging_hash(telegram_id)}, "
                         f"language: {new_user_language}")

    bot.delete_message(call.message.chat.id, call.message.message_id)  # delete message with list of languages


def restart_language_after_changes(call) -> None:
    """
    Since the start command is called with the message parameter,
    and this object cannot be obtained from the callback function,
    then this function was made as a reboot of the buttons after changing the language.
    """
    telegram_id: int = call.from_user.id
    user_language: str = check_user_language(telegram_id)
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup_1.add(KeyboardButton('/start'))
    # The bot needs to be restarted for it to work correctly (maybe it’s worth reconsidering this in the future)
    bot.send_message(call.message.chat.id,
                     f"{receive_translation(user_language, "start_after_change_language")}\n"
                     f"{receive_translation(user_language, "data_is_safe")}",
                     reply_markup=markup_1)


@connect_defer_close_db
def get_my_token(db_connection, message, user_language: str) -> None:
    telegram_id: int = message.from_user.id
    token: str = db_connection.get_token_by_telegram_id(telegram_id)
    token: str = token if token else receive_translation(user_language, 'unknown')
    bot.send_message(message.chat.id, f"{receive_translation(user_language, "group_token")}:")
    bot.send_message(message.chat.id, token)


@connect_defer_close_db
def start_transaction(db_connection, message, user_language: str, is_negative: bool) -> None:
    text_key: str = 'enter_expense' if is_negative else 'enter_income'
    msg = bot.send_message(message.chat.id, f"{receive_translation(user_language, text_key)}:")
    feature_is_active: bool = db_connection.get_feature_status_del_msg_after_transaction(message.from_user.id)
    msg_del_obj = StorageMsgIdForDeleteAfterOperation(feature_is_active)
    msg_del_obj.append(msg.id)
    bot.register_next_step_handler(message, process_add_date_for_transfer, is_negative, msg_del_obj)


def process_add_date_for_transfer(message, is_negative: bool, msg_del_obj: StorageMsgIdForDeleteAfterOperation) -> None:
    """
    Adds income and expense to the database.
    Accepts an unvalidated value,
    performs validation and enters it into the database.

    Args:
        message:
        is_negative (bool): False if X > 0 (add_income), True if X < 0 (add_expense)
        X = 0 - will be rejected by the validator
        msg_del_obj:

    Returns: None
    """
    msg_del_obj.append(message.message_id)
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
        msg = bot.send_message(message.chat.id, f"{receive_translation(user_language, "set_date")} (DD/MM/YYYY)",
                               reply_markup=markup_1)
        msg_del_obj.append(msg.id)
        bot.register_next_step_handler(message, process_add_category_for_transfer, value, user_language, msg_del_obj)
    else:
        bot.send_message(message.chat.id, receive_translation(user_language, 'invalid_value'))


def process_add_category_for_transfer(message, value: int, user_language: str,
                                      msg_del_obj: StorageMsgIdForDeleteAfterOperation) -> None:
    msg_del_obj.append(message.message_id)
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    button_labels: tuple = get_category_button_labels(user_language)
    buttons: list = [KeyboardButton(label) for label in button_labels]  # assembling buttons from the tuple above
    markup_1.add(*buttons)

    record_date: str = message.text
    record_date_is_valid: bool = asyncio_run(date_validation(record_date))  # DD/MM/YYYY

    if record_date_is_valid:
        msg = bot.send_message(message.chat.id, f"{receive_translation(user_language, "select_category")}:",
                               reply_markup=markup_1)
        msg_del_obj.append(msg.id)
        bot.register_next_step_handler(message, process_add_description_for_transfer, value,
                                       record_date, user_language, msg_del_obj)
    else:
        bot.send_message(message.chat.id, receive_translation(user_language, 'invalid_date'))
        reply_buttons(message)


def process_add_description_for_transfer(message, value: int, record_date: str, user_language: str,
                                         msg_del_obj: StorageMsgIdForDeleteAfterOperation) -> None:
    msg_del_obj.append(message.message_id)
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    btn1 = KeyboardButton(receive_translation(user_language, 'no_description'))
    markup_1.add(btn1)
    category: str = message.text

    if category_validation(user_language, category):
        msg = bot.send_message(message.chat.id, receive_translation(user_language, 'add_description'),
                               reply_markup=markup_1)
        msg_del_obj.append(msg.id)
        bot.register_next_step_handler(message, process_transfer_final, value, record_date,
                                       category, user_language, msg_del_obj)
    else:
        bot.send_message(message.chat.id, receive_translation(user_language, 'invalid_category'))
        reply_buttons(message)
        logger_bot.info(f'User entered an incorrect category. Category: {category}')


@connect_defer_close_db
def process_transfer_final(
        db_connection,
        message,
        value: int,
        record_date: str,
        category: str,
        user_language: str,
        msg_del_obj: StorageMsgIdForDeleteAfterOperation
) -> None:
    msg_del_obj.append(message.message_id)
    telegram_id: int = message.from_user.id
    description: str = message.text

    if description == receive_translation(user_language, 'no_description'):
        description: str = ""

    if description_validation(description):
        if db_connection.add_transaction_to_db(value, record_date, category, description, telegram_id=telegram_id):
            bot.send_message(chat_id := message.chat.id, f"{receive_translation(user_language, 'entry_add_success')}!")
            msg_del_obj.delete_messages(bot, chat_id)
        else:
            bot.send_message(message.chat.id, f"{receive_translation(user_language, 'entry_add_error')}\n"
                                              f"{receive_translation(user_language, 'contact_support')}")
    else:
        bot.send_message(message.chat.id, receive_translation(user_language, 'invalid_value'))

    table_manage_get_buttons(message)


def delete_record(message, user_language: str) -> None:
    bot.send_message(message.chat.id, f"{receive_translation(user_language, 'entry_record_id')}:")
    bot.register_next_step_handler(message, process_delete_record, user_language)


@connect_defer_close_db
def process_delete_record(db_connection, message, user_language: str):
    telegram_id: int = message.from_user.id
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = KeyboardButton(f"❌ {receive_translation(user_language, 'del_record')}")
    btn2 = KeyboardButton(f"↩️ {receive_translation(user_language, 'back_to_menu')}")
    markup_1.add(btn1, btn2)
    transaction_id: int = value_validation(message.text)

    if transaction_id:
        group_id: int = db_connection.get_group_id_by_telegram_id(telegram_id)
        if group_id and db_connection.check_record_id_is_exist(group_id, transaction_id):
            db_connection.process_delete_transaction_record(group_id, transaction_id)
            bot.send_message(message.chat.id, f"{receive_translation(user_language, 'success')}!")
        else:
            bot.send_message(message.chat.id, receive_translation(user_language, 'enry_record_id_error'),
                             reply_markup=markup_1)
    else:
        bot.send_message(message.chat.id, receive_translation(user_language, 'invalid_value'),
                         reply_markup=markup_1)


def registration(message, user_language: str, res: bool) -> None:
    if not res:  # Checking whether the user is already registered and accidentally ended up in this menu.
        bot.send_message(message.chat.id, f"{receive_translation(user_language, 'enter_username')}:")
        bot.register_next_step_handler(message, process_username, user_language)
    else:
        bot.send_message(message.chat.id, f"{receive_translation(user_language, 'already_registered')}!")
        reply_buttons(message)


def process_username(message, user_language: str):
    username: str = message.text
    if asyncio_run(username_validation(username)):
        bot.send_message(message.chat.id, f"{receive_translation(user_language, 'enter_password')}:")
        bot.register_next_step_handler(message, process_psw, username, user_language)
    else:
        bot.send_message(message.chat.id, receive_translation(user_language, 'invalid_username'))


def process_psw(message, username: str, user_language: str):
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton("None")
    markup_1.add(btn1)

    psw: str = message.text
    if asyncio_run(password_validation(psw)):
        psw_salt: str = get_salt()
        psw_hash: str = getting_hash(psw, psw_salt)
        bot.send_message(message.chat.id, f"{receive_translation(user_language, "enter_token")}\n"
                                          f"{receive_translation(user_language, "none_token")}",
                         reply_markup=markup_1)
        bot.register_next_step_handler(message, process_token, username, psw_hash, psw_salt, user_language)
    else:
        bot.send_message(message.chat.id, receive_translation(user_language, 'invalid_password_format'))
        reply_buttons(message)


@connect_defer_close_db
def process_token(db_connection, message, username: str, psw_hash: str, psw_salt: str, user_language: str):
    telegram_id: int = message.from_user.id
    token: str = message.text
    res, status = user_registration(db_connection, token, telegram_id, username, psw_salt, psw_hash)
    res: bool
    status: str  # if the group is successfully created, this is a token
    return_msg: str = ''

    if res:
        bot.send_message(message.chat.id, receive_translation(user_language, 'congratulations'))
        bot.send_sticker(message.chat.id, Stickers.get_sticker_by_id('id_4'))
        if status:
            bot.send_message(message.chat.id, f"{receive_translation(user_language, "your")} token:\n{status}")
        reply_menu_buttons_register(message)
        return

    if status == 'create_new_user_or_group_error':
        return_msg += (f"{receive_translation(user_language, "create_new_user_error")}. "
                       f"{receive_translation(user_language, "contact_support")}")
    elif status == 'group_not_exist':
        return_msg += receive_translation(user_language, 'group_not_exist')
    elif status == 'group_is_full':
        return_msg += receive_translation(user_language, 'group_is_full')
    elif status == 'invalid_token_format':
        return_msg += receive_translation(user_language, 'invalid_token_format')

    bot.send_message(message.chat.id, return_msg)
    reply_menu_buttons_not_register(message)
    return


@connect_defer_close_db
def view_table(db_connection, message, res: bool, user_language: str) -> None:
    chat_id: int = message.chat.id
    # https://core.telegram.org/bots/api#sendchataction
    # https://pytba.readthedocs.io/en/latest/sync_version/index.html#telebot.TeleBot.send_chat_action
    bot.send_chat_action(chat_id, 'typing')  # returns True on success
    telegram_id: int = message.from_user.id
    if res:  # user authorization check
        group_id: int = db_connection.get_group_id_by_telegram_id(telegram_id)
        data: tuple = db_connection.select_data_for_household_table(group_id, 10)
        if data:
            # Generating a single message from nested lists of the 'data' tuple
            category_data: tuple = get_category_translate(user_language)
            bot.send_message(chat_id,
                             '\n'.join([f"ID: {table_entry[0]}\n"
                                        f"{category_data[0]}: {table_entry[1]}\n"
                                        f"{category_data[1]}: {table_entry[2]}\n"
                                        f"{category_data[2]}: {table_entry[3]}\n"
                                        f"{category_data[3]}: {table_entry[4]}\n"
                                        f"{category_data[4]}: {table_entry[5]}\n"
                                        f"{category_data[5]}: {table_entry[6]}\n\n"
                                        for table_entry in data]))
        else:
            bot.send_message(chat_id, receive_translation(user_language, 'table_is_empty'))


@connect_defer_close_db
def get_csv(db_connection, message, user_language: str) -> None:
    chat_id: int = message.chat.id
    # https://core.telegram.org/bots/api#sendchataction
    # https://pytba.readthedocs.io/en/latest/sync_version/index.html#telebot.TeleBot.send_chat_action
    bot.send_chat_action(chat_id, 'upload_document')  # returns True on success
    telegram_id: int = message.from_user.id
    group_id: int = db_connection.get_group_id_by_telegram_id(telegram_id)
    # to be able to call a function from any file
    group_uuid: str = db_connection.get_group_transaction_uuid(group_id)
    file_path: str = path.join(path.dirname(__file__), f'csv_tables/{group_id}_{group_uuid}.csv')
    # 10_000 row limit
    table_data: tuple[tuple, ...] = db_connection.select_data_for_household_table(group_id, 0)
    if table_data:
        try:
            csv_obj = CsvFileWithTable(file_path, table_data)
            if not check_csv_is_actual(group_id, group_uuid):
                csv_obj.create_csv_file()
            file_size: float = csv_obj.get_file_size_kb()
            file_checksum: str = csv_obj.get_file_checksum()
            with open(f'csv_tables/{group_id}_{group_uuid}.csv', 'rb') as csv_table_file:
                caption: str = (f"{receive_translation(user_language, 'file_size')}: "
                                f"{'{:.3f}'.format(file_size)} kB\n\n"
                                f"{receive_translation(user_language, 'hashsum')} "
                                f"(sha-256): {file_checksum}")
                bot.send_document(chat_id, csv_table_file, caption=caption)
        except FileNotFoundError as err:
            bot.send_message(chat_id, receive_translation(user_language, 'csv_not_found_error'))
            logger_bot.error(f"CSV FileNotFoundError => {err}. "
                             f"TelegramID: {logging_hash(telegram_id)}, "
                             f"group #{group_id}")
        # when trying to run an operation without access rights
        except PermissionError as err:
            bot.send_message(chat_id, receive_translation(user_language, 'csv_not_found_error'))
            logger_bot.error(f"CSV PermissionError => {err}. "
                             f"TelegramID: {logging_hash(telegram_id)}, "
                             f"group #{group_id}")
        except ValueError as err:
            bot.send_message(chat_id, receive_translation(user_language, 'invalid_data_table_for_csv'))
            logger_bot.error(f"CSV ValueError => {err}. "
                             f"TelegramID: {logging_hash(telegram_id)}, "
                             f"group #{group_id}")
        else:
            logger_bot.info(f"CSV: SUCCESS. "
                            f"TelegramID: {logging_hash(telegram_id)}, "
                            f"group #{group_id}. "
                            f"File size: {'{:.3f}'.format(file_size)} kB, "
                            f"hashsum: {file_checksum}")
    else:
        bot.send_message(message.chat.id, receive_translation(user_language, 'table_is_empty'))


@connect_defer_close_db
def get_group_users(db_connection, message, user_language: str):
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
    group_id: int = db_connection.get_group_id_by_telegram_id(telegram_id)
    group_owner_username: str = db_connection.get_group_owner_username_by_group_id(group_id)
    group_users_list: tuple = db_connection.get_group_usernames(group_id)
    group_users_str: str = '\n'.join(
        f"{user} ({receive_translation(user_language, 'owner')})"
        if user == group_owner_username
        else f"{user}"
        for user in group_users_list
    )
    bot.send_message(message.chat.id, group_users_str)


@connect_defer_close_db
def change_owner(db_connection, message, user_language: str):
    telegram_id: int = message.from_user.id
    group_id: int = db_connection.get_group_id_by_telegram_id(telegram_id)
    group_owner_username: str = db_connection.get_group_owner_username_by_group_id(group_id)
    username: str = db_connection.get_username_by_telegram_id(telegram_id)
    if compare_digest(group_owner_username, username):
        group_users_list: tuple = db_connection.get_group_usernames(group_id)
        # if there are no users in the group except the owner
        if len(group_users_list) == 1:
            bot.send_message(message.chat.id, receive_translation(user_language, 'small_group_exception'))
        else:
            # List of users as a string without group owner
            group_users_str_without_owner: str = '\n'.join(
                f"{user}" for user in group_users_list if user != group_owner_username
            )
            bot.send_message(message.chat.id,
                             f"{receive_translation(user_language, 'username_new_owner')}:\n"
                             f"{group_users_str_without_owner}")
            bot.register_next_step_handler(message, process_change_owner, group_id, user_language)
    else:
        bot.send_message(message.chat.id, receive_translation(user_language, 'not_owner_exception'))


@connect_defer_close_db
def process_change_owner(db_connection, message, group_id: int, user_language: str) -> None:
    telegram_id: int = message.from_user.id
    new_owner_username: str = message.text
    telegram_id_new_owner: int = db_connection.get_telegram_id_by_username(new_owner_username)
    user_from_current_group: bool = db_connection.get_group_id_by_telegram_id(telegram_id_new_owner) == group_id
    user_is_owner: bool = db_connection.check_user_is_group_owner_by_telegram_id(telegram_id_new_owner, group_id)

    if user_is_owner:
        bot.send_message(message.chat.id, receive_translation(user_language, 'current_owner_exception'))
    elif user_from_current_group:
        if db_connection.update_group_owner(telegram_id_new_owner, group_id):
            bot.send_message(message.chat.id, receive_translation(user_language, 'owner_has_been_changed'))
            logger_bot.info(f"Group owner changed: group #{group_id},"
                            f" new owner username: {logging_hash(new_owner_username)}")
        else:
            bot.send_message(message.chat.id, receive_translation(user_language, 'error_change_owner'))
            logger_bot.error(f"Owner change error. group #{group_id}, current owner: {logging_hash(telegram_id)},"
                             f" desired owner: {logging_hash(telegram_id_new_owner)} "
                             f"- this user is a member of the group.")
    else:
        bot.send_message(message.chat.id, f"{receive_translation(user_language, 'check_correct_username')}\n"
                                          f"{receive_translation(user_language, 'unknown_user_in_group')}")
        logger_bot.error(f"Owner change error. group #{group_id}, current owner: {logging_hash(telegram_id)},"
                         f" desired owner: {logging_hash(new_owner_username)} "
                         f"- this user is not a member of the group.")
    group_settings_get_buttons(message)


@connect_defer_close_db
def delete_account(db_connection, message, user_language: str):
    telegram_id: int = message.from_user.id
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton(f"👍 {receive_translation(user_language, 'YES')}")
    btn2 = KeyboardButton(f"👎 {receive_translation(user_language, 'NO')}")
    markup_1.add(btn1, btn2)
    group_id: int = db_connection.get_group_id_by_telegram_id(telegram_id)
    user_is_owner: bool = db_connection.check_user_is_group_owner_by_telegram_id(telegram_id, group_id)
    if user_is_owner:
        bot.send_message(message.chat.id, receive_translation(user_language, 'owner_try_delete_account'))
    else:
        bot.send_message(message.chat.id, receive_translation(user_language, 'confirmation_delete'),
                         reply_markup=markup_1)
        bot.register_next_step_handler(message, process_delete_account, user_language)


@connect_defer_close_db
def process_delete_account(db_connection, message, user_language: str):
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = KeyboardButton('/start')
    markup_1.add(btn1)
    telegram_id: int = message.from_user.id
    user_choice: str = message.text
    if user_choice == f"👍 {receive_translation(user_language, "YES")}":
        # removing a user from the cache
        UserRegistrationStatusCache.delete_data_from_cache(telegram_id)
        db_connection.delete_user_from_group_by_telegram_id(telegram_id)
        bot.send_message(message.chat.id, receive_translation(user_language, 'parting'))
        bot.send_message(message.chat.id, receive_translation(user_language, 'account_is_deleted'),
                         reply_markup=markup_1)
        logger_bot.info(f"User deleted the account. TelegramID: {logging_hash(telegram_id)}")
        start(message)

    elif user_choice == f"👎 {receive_translation(user_language, 'NO')}":
        bot.send_message(message.chat.id, receive_translation(user_language, 'stay_with_us'))
        group_settings_get_buttons(message)

    else:
        bot.send_message(message.chat.id, receive_translation(user_language, 'unknown_message'))
        logger_bot.info(f'Unrecognized message when deleting an account. '
                        f'TelegramID: {logging_hash(telegram_id)}, message: {user_choice}')
        group_settings_get_buttons(message)


@connect_defer_close_db
def delete_user(db_connection, message, user_language: str):
    telegram_id: int = message.from_user.id
    group_id: int = db_connection.get_group_id_by_telegram_id(telegram_id)
    group_owner: str = db_connection.get_group_owner_username_by_group_id(group_id)
    user_is_owner: bool = db_connection.check_user_is_group_owner_by_telegram_id(telegram_id, group_id)
    if user_is_owner:
        group_users_list: tuple = db_connection.get_group_usernames(group_id)
        if len(group_users_list) == 1:  # If there are no users in the group except the owner
            bot.send_message(message.chat.id,
                             f"{receive_translation(user_language, 'exception_one_user_in_group')}\n"
                             f"{receive_translation(user_language, 'select_to_delete')}")
        else:
            # List of users as a string without group owner
            group_users_str_without_owner: str = '\n'.join(f"{user}" for user in group_users_list
                                                           if user != group_owner)
            bot.send_message(message.chat.id, f"{receive_translation(user_language, 'select_new_owner')}\n"
                                              f"{group_users_str_without_owner}")
            bot.register_next_step_handler(message, process_delete_user, group_id, group_users_list, user_language)
    else:
        bot.send_message(message.chat.id, receive_translation(user_language, 'owner_privileges'))


@connect_defer_close_db
def process_delete_user(db_connection, message, group_id: int, group_users_list: tuple, user_language: str) -> None:
    username_user_to_delete: str = message.text
    telegram_id_user_to_delete: int = db_connection.get_telegram_id_by_username(username_user_to_delete)
    user_to_delete_is_owner: bool = db_connection.check_user_is_group_owner_by_telegram_id(telegram_id_user_to_delete,
                                                                                           group_id)

    if user_to_delete_is_owner:
        bot.send_message(message.chat.id, receive_translation(user_language, 'current_owner_exception'))
    elif username_user_to_delete not in group_users_list:
        bot.send_message(message.chat.id,
                         f"{receive_translation(user_language, 'check_correct_username')}\n"
                         f"{receive_translation(user_language, 'unknown_user_in_group')}")
    else:
        # removing a user from the cache
        UserRegistrationStatusCache.delete_data_from_cache(telegram_id_user_to_delete)
        if db_connection.delete_user_from_group_by_telegram_id(telegram_id_user_to_delete):
            bot.send_message(message.chat.id, receive_translation(user_language, 'user_removed'))
            logger_bot.info(f"'User {logging_hash(username_user_to_delete)}' "
                            f"deleted by group owner from group #{group_id}")
        else:
            bot.send_message(message.chat.id, receive_translation(user_language, 'error_user_delete'))
            logger_bot.warning(f"Error removing user "
                               f"'{logging_hash(username_user_to_delete)}' "
                               f"from group #{group_id}")
    group_settings_get_buttons(message)


@connect_defer_close_db
def delete_group(db_connection, message, user_language: str) -> None:
    telegram_id: int = message.from_user.id
    markup_1 = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = KeyboardButton(f"🌧️ {receive_translation(user_language, 'YES')}")
    btn2 = KeyboardButton(f"🌤️ {receive_translation(user_language, 'NO')}")
    markup_1.add(btn1, btn2)
    group_id: int = db_connection.get_group_id_by_telegram_id(telegram_id)
    user_is_owner: bool = db_connection.check_user_is_group_owner_by_telegram_id(telegram_id, group_id)

    if user_is_owner:
        bot.send_message(message.chat.id,
                         f"{receive_translation(user_language, 'are_you_sure')}\n"
                         f"{receive_translation(user_language, 'delete_table')}",
                         reply_markup=markup_1)
        bot.register_next_step_handler(message, process_delete_group, group_id, user_language)
    else:
        bot.send_message(message.chat.id, receive_translation(user_language, 'not_deleted_by_owner'))


@connect_defer_close_db
def process_delete_group(db_connection, message, group_id: int, user_language: str) -> None:
    telegram_id: int = message.from_user.id
    user_choice: str = message.text
    # the user confirmed the deletion of the group
    if user_choice == f"🌧️ {receive_translation(user_language, 'YES')}":
        # get a list of telegram_id for each user of the group:
        telegram_ids_of_group_users: tuple = db_connection.get_group_telegram_ids(group_id)
        # clearing group users from the cache
        UserRegistrationStatusCache.delete_group_trigger(telegram_ids_of_group_users)
        db_connection.delete_group_with_users(group_id)
        bot.send_message(message.chat.id, receive_translation(user_language, 'parting'))
        bot.send_message(message.chat.id, receive_translation(user_language, 'remove_completed'))
        logger_bot.info(f"User deleted the group. "
                        f"TelegramID: {logging_hash(telegram_id)}, "
                        f"group #{group_id}")
        start(message)
    # the user changed his mind about deleting the group
    elif user_choice == f"🌤️ {receive_translation(user_language, 'NO')}":
        bot.send_message(message.chat.id, receive_translation(user_language, 'stay_with_us'))
        group_settings_get_buttons(message)
    # the user entered an unexpected message
    else:
        bot.send_message(message.chat.id, receive_translation(user_language, 'unknown_message'))
        logger_bot.info(f"Unrecognized message when deleting group. "
                        f"TelegramID: {logging_hash(telegram_id)}, "
                        f"message: {user_choice}, "
                        f"group #{group_id}")
        group_settings_get_buttons(message)


# TODO reuse func
@connect_defer_close_db
def get_str_with_group_users(db_connection, telegram_id: int, with_owner: bool) -> str:
    user_language: str = check_user_language(telegram_id)
    group_id: int = db_connection.get_group_id_by_telegram_id(telegram_id)
    group_owner_username: str = db_connection.get_group_owner_username_by_group_id(group_id)
    group_users_list: tuple = db_connection.get_group_usernames(group_id)

    if with_owner:
        res: str = '\n'.join(
            f'{user} ({receive_translation(user_language, 'owner')})'
            if user == group_owner_username
            else
            f'{user}'
            for user in group_users_list
        )
    else:
        res: str = '\n'.join(
            f'{user}'
            for user in group_users_list
            if user != group_owner_username
        )
    return res


@connect_defer_close_db
def user_is_registered(db_connection, telegram_id: int) -> bool:
    """
    We check whether the user is registered in the project.
    Since the user may accidentally end up in a menu
    intended only for registered users.
    """
    user_in_cache: bool = UserRegistrationStatusCache.get_cache_data(telegram_id)

    if user_in_cache:  # if you found data in the cache or received a response from the database
        # update date of the last user activity in database
        db_connection.update_user_last_login_by_telegram_id(telegram_id)
    else:  # if the data is not found in the cache
        if db_connection.check_telegram_id_is_exist(telegram_id):  # found user in database
            # updating the data in the cache
            UserRegistrationStatusCache.input_cache_data(telegram_id)
            user_in_cache = True

    return user_in_cache


@connect_defer_close_db
def check_user_language(db_connection, telegram_id: int) -> str:
    """
    Makes a request to the database via the get_user_language function.
    The telegram id of the user taken from the message is used.
    """
    language: str = UserLanguageCache.get_cache_data(telegram_id)
    if not language:
        language: str = db_connection.get_user_language(telegram_id)
        UserLanguageCache.input_cache_data(telegram_id, language)
    return language


def get_answer_for_unregistered_user(message, telegram_id: int, user_language: str, functional: str):
    bot.send_message(message.chat.id, receive_translation(user_language, 'not_register'))
    bot.send_sticker(message.chat.id, Stickers.get_sticker_by_id('id_5'))
    logger_bot.info(f'{functional} Unregistered user interaction. TelegramID: {logging_hash(telegram_id)}')
    reply_menu_buttons_not_register(message)


# pylint: disable=too-many-branches, too-many-function-args
@bot.message_handler(content_types=['text'])
def text(message) -> None:
    telegram_id: int = message.from_user.id
    user_language: str = check_user_language(telegram_id)
    res: bool = user_is_registered(telegram_id)

    if message.text == f"📬 {receive_translation(user_language, 'register')}":
        registration(message, user_language, res)
    elif message.text == f"⭐ {receive_translation(user_language, 'premium')}":
        premium(message, user_language)
    elif message.text == f"🔐 {receive_translation(user_language, 'get_my_token')}":
        get_my_token(message, user_language)
    elif message.text == f"💵 {receive_translation(user_language, 'table_manage')}":
        if res:
            table_manage_get_buttons(message)
        else:
            reply_menu_buttons_not_register(message)
    elif message.text == f"💻 {receive_translation(user_language, 'group_settings')}":
        if res:
            group_settings_get_buttons(message)
        else:
            reply_menu_buttons_not_register(message)
    elif message.text in (f"↩️ {receive_translation(user_language, 'back')}",
                          f"↩️ {receive_translation(user_language, 'back_to_menu')}"):
        reply_buttons(message)
    # if an unauthorized user tries to perform an action that is only available after authorization
    elif not res:
        bot.send_message(message.chat.id, receive_translation(user_language, 'not_register'))
        bot.send_sticker(message.chat.id, Stickers.get_sticker_by_id('id_5'))
        logger_bot.info(f'Unregistered user interaction. TelegramID: {logging_hash(telegram_id)}')
    elif res:
        if message.text == f"📖 {receive_translation(user_language, 'view_table')}":
            view_table(message, res, user_language)
        elif message.text == f"📈 {receive_translation(user_language, 'add_income')}":
            start_transaction(message, user_language, False)
        elif message.text == f"📉 {receive_translation(user_language, 'add_expense')}":
            start_transaction(message, user_language, True)
        elif message.text == f"❌ {receive_translation(user_language, 'del_record')}":
            delete_record(message, user_language)
        elif message.text == f"🗃️ {receive_translation(user_language, 'get_csv')}":
            get_csv(message, user_language)
        elif message.text == f"🌍 {receive_translation(user_language, 'group_users')}":
            get_group_users(message, user_language)
        elif message.text == f"📊 {receive_translation(user_language, 'get_diagram')}":
            get_diagram(message, user_language)
        elif message.text == f"🗑️ {receive_translation(user_language, 'delete_account')}":
            delete_account(message, user_language)
        elif message.text == f"🚫 {receive_translation(user_language, 'delete_group')}":
            delete_group(message, user_language)
        elif message.text == f"🔑 {receive_translation(user_language, 'change_owner')}":
            change_owner(message, user_language)
        elif message.text == f"🤖 {receive_translation(user_language, 'delete_user')}":
            delete_user(message, user_language)
    else:
        bot.send_message(message.chat.id, receive_translation(user_language, 'misunderstanding'))


bot.polling(none_stop=True)
