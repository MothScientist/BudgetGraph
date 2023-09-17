import telebot
from telebot import types
from os import getenv
from dotenv import load_dotenv

# Database
from database_control import FDataBase, connect_db, close_db_bot

# Validators
from validators.input_number import input_number


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
        connection = connect_db()
        bot_db = FDataBase(connection)
        res: bool | str = bot_db.get_username_by_tg_link("https://t.me/" + message.from_user.username)

        if res:
            bot_db.update_user_last_login(res)
            bot.send_message(message.chat.id, f"Hello, {res}!\n"
                                              f"We recognized you. Welcome!", reply_markup=markup_1)
        else:
            bot.send_message(message.chat.id, f"Hello, {message.from_user.first_name} {message.from_user.last_name}!\n"
                                              f"We didn't recognize you. Would you like to register in the project?",
                             reply_markup=markup_2)

        close_db_bot(connection)

    @bot.message_handler(commands=['registration'])
    def registration(message):
        pass

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
        connection = connect_db()
        bot_db = FDataBase(connection)
        token = bot_db.get_token_by_tg_link("https://t.me/" + message.from_user.username)
        close_db_bot(connection)
        bot.send_message(message.chat.id, f"Your group token:")
        bot.send_message(message.chat.id, f"{token}")

    @bot.message_handler(commands=['add_income'])
    def add_income(message):
        bot.send_message(message.chat.id, f"Enter the amount of income:")
        bot.register_next_step_handler(message, process_transfer, False)

    @bot.message_handler(commands=['add_expense'])
    def add_expense(message):
        bot.send_message(message.chat.id, f"Enter the amount of expense:")
        bot.register_next_step_handler(message, process_transfer, True)

    def process_transfer(message, is_negative: bool = False):
        """

        :param message:
        :param is_negative: False if X > 0 (add_income), True if X < 0 (add_expense)
        :return:
        """
        transfer: str = message.text
        transfer: int | bool = input_number(transfer)

        if transfer:
            connection = connect_db()
            bot_db = FDataBase(connect_db())
            group_id: int = bot_db.get_group_id_by_tg_link("https://t.me/" + message.from_user.username)
            username: str = bot_db.get_username_by_tg_link("https://t.me/" + message.from_user.username)
            if is_negative:
                bot_db.add_monetary_transaction_to_db(f"budget_{group_id}", username, transfer*(-1))
            else:
                bot_db.add_monetary_transaction_to_db(f"budget_{group_id}", username, transfer)

            close_db_bot(connection)
            bot.send_message(message.chat.id, "Data added successfully.")

    @bot.message_handler(commands=['view_table'])
    def view_table(message):
        pass

    @bot.message_handler(content_types=['text'])
    def text(message):
        if message.text == "❓ Help":
            help(message)

        elif message.text == "📎 Link to GitHub":
            project_github(message)

        elif message.text == "💻 My Telegram link":
            my_link(message)

        elif message.text == "🤡 I want to register":
            registration(message)

        elif message.text == "🔐 Get my token":
            get_token(message)

        elif message.text == "📖 View table":
            view_table(message)

        elif message.text == "📈 Add income":
            add_income(message)

        elif message.text == "📉 Add expense":
            add_expense(message)

    bot.polling(none_stop=True)


if __name__ == '__main__':
    main()
