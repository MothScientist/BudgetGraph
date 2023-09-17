from flask import g
import sqlite3
import os
from dotenv import load_dotenv
from token_generation import get_token
from validators.table_name import table_name_validator

load_dotenv()  # Load environment variables from .env file
db_path = os.getenv("DATABASE")


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

# Database sampling methods (SELECT)

    def get_username_by_tg_link(self, tg_link: str) -> bool | str:
        """
        Finds a user in the Users table by telegram_link value
        return: username or False
        """
        try:
            self.__cur.execute("""SELECT username FROM Users WHERE telegram_link = ?""", (tg_link,))
            res = self.__cur.fetchone()

            if res:  # If a user with this link is found
                return res[0]
            else:
                return False

        except sqlite3.Error as e:
            print(str(e))

    def get_group_id_by_token(self, token: str) -> int:
        """
        search for a group by its token
        return: the id value of this group
        """
        try:
            self.__cur.execute("""SELECT id FROM Groups WHERE token = ?""", (token,))
            res = self.__cur.fetchone()
            if res:
                return res[0]
        except sqlite3.Error as e:
            print(str(e))

    def get_token_by_username(self, username: str) -> str:
        """
        Obtaining a group token using username produces a query with a subquery in 2 tables.
        """
        try:
            self.__cur.execute("""SELECT token FROM Groups WHERE id = 
                                 (SELECT group_id FROM Users WHERE username = ?)""", (username,))
            res = self.__cur.fetchone()
            return res[0]

        except sqlite3.Error as e:
            print(str(e))

    def get_token_by_telegram_link(self, tg_link: str):
        """

        :return:
        """
        try:
            self.__cur.execute("""SELECT token FROM Groups WHERE id = 
                                 (SELECT group_id FROM Users WHERE telegram_link = ?)""", (tg_link,))
            res = self.__cur.fetchone()
            return res[0]

        except sqlite3.Error as e:
            print(str(e))

    def get_salt_by_username(self, username: str) -> str | bool:
        """
        necessary for hashing the user's password during authorization.
        return: str - if salt is found. bool (false) - if information on this user is not in the database.
        """
        try:
            self.__cur.execute("""SELECT psw_salt FROM Users WHERE username = ?""", (username,))
            res = self.__cur.fetchone()
            if res:
                return str(res[0])
            else:
                return False

        except sqlite3.Error as e:
            print(str(e))

    def get_id_by_username(self, username: str, tg_link: str) -> bool:
        """
        Since the username and telegram_link fields are unique,
        additional verification is required so that errors do not appear in the future when working with the database.
        return: True - if the data is found in the database, False - if both parameters are not found in the database.
        """
        try:
            self.__cur.execute("""SELECT id FROM Users WHERE telegram_link = ?""", (tg_link,))
            res_link = self.__cur.fetchone()

            self.__cur.execute("""SELECT id FROM Users WHERE username = ?""", (username,))
            res_username = self.__cur.fetchone()

            if res_link or res_username:  # If a user with this link or name is found
                return True
            else:
                return False

        except sqlite3.Error as e:
            print(str(e))

    def auth_by_username(self, username: str, psw_hash: str, token: str) -> bool:
        """
        full process of user confirmation during authorization.
        the whole process is initialized with the username
        return: True if the user was successfully found and the data was confirmed, False otherwise.
        """
        try:
            self.__cur.execute("""SELECT username FROM Users WHERE username = ? AND password_hash = ? AND EXISTS (
                    SELECT token FROM Groups WHERE Groups.id = Users.group_id AND token = ?)""",
                               (username, psw_hash, token))
            res = self.__cur.fetchone()
            if res:
                return True
            else:
                return False

        except sqlite3.Error as e:
            print(str(e))

    def select_data_for_household_table(self, table_name: str) -> list:
        try:
            self.__cur.execute(f"SELECT * FROM {table_name} ORDER BY id DESC LIMIT 15")
            result = self.__cur.fetchall()
            result_list = [list(row) for row in result]
            return result_list

        except sqlite3.Error as e:
            print(str(e))

# Methods for inserting data into a database (INSERT)

    def add_user_to_db(self, username: str, psw_salt: str, psw_hash: str, group_id: int, tg_link: str) -> bool:
        """
        adding a new user to the Users table
        return: True if the addition was successful and False otherwise.
        """
        try:
            self.__cur.execute("INSERT INTO Users "
                               "VALUES(NULL, ?, ?, ?, ?, ?, strftime('%d-%m-%Y %H:%M:%S', 'now', 'localtime'))",
                               (username, psw_salt, psw_hash, group_id, tg_link,))
            self.__db.commit()

        except sqlite3.Error as e:
            print(str(e))
            return False

        else:  # Executed if the try block executed without errors.
            return True

    def add_monetary_transaction_to_db(self, table_name: str, username: str, amount: int, description: str = "")\
            -> bool:
        """
        Submits the "add_expense" and "add_income" forms to the database.
        """
        if not table_name_validator(table_name):  # Additional check of table title format
            return False
        try:
            self.__cur.execute(
                f"INSERT INTO {table_name} VALUES (NULL, COALESCE((SELECT SUM(transfer) FROM {table_name}), 0) + ?,"
                f" ?, ?, strftime('%d-%m-%Y %H:%M:%S', 'now', 'localtime'), ?)",
                (amount, username, amount, description))
            self.__db.commit()

        except sqlite3.Error as e:
            print(str(e))

        else:  # Executed if the try block executed without errors.
            return True

        return False

    def create_new_group(self, owner: str) -> str | bool:
        """
        creating a new group in the Groups table
        :param owner: link to the telegram of the user who initiates the creation of the group
        :return: token generated by external function (returns False in case of error)
        """
        try:
            token = get_token()
            self.__cur.execute("INSERT INTO Groups VALUES(NULL, ?, ?)", (owner, token,))
            self.__db.commit()

        except sqlite3.Error as e:
            print(str(e))
            return False

        else:
            return token

# Methods for updating data in a database (UPDATE)

    def update_user_last_login(self, username: str) -> None:
        """
        changes the user's last login time in the last_login column in the Users table
        :param username:
        :return: None
        """
        try:
            self.__cur.execute("""UPDATE Users SET last_login = strftime('%d-%m-%Y %H:%M:%S', 'now', 'localtime') 
            WHERE username = ?""", (username,))
            self.__db.commit()

        except sqlite3.Error as e:
            print(str(e))


def connect_db():
    """
    Connects to the database
    :return: connection
    """
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    except sqlite3.Error as e:
        print(str(e))


def get_db():
    """
    A function required to establish a connection to the database.
    """
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
        print("Database connection: OK")
    return g.link_db


def close_db(error) -> None:
    """
    Required to close the connection to the database.

    Used in the main application file through the app.teardown_appcontext function.
    """
    if hasattr(g, "link_db"):
        g.link_db.close()
        print("Database connection: CLOSED")


def create_db() -> None:
    """
    Creates 2 main tables: Users and Groups, using a .sql file describing their structures.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()

        with open("create_db.sql", 'r') as file:
            cursor.executescript(file.read())

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(str(e))


def create_table_group(table_name) -> None:
    """
    creates a table in the database called budget_? (id, total, username, transfer, date_time, description)

    contains table_name_validator -> to protect against sql injection, validation of the table_name parameter is needed
    :param table_name: "budget_?"
    :return: None
    """
    try:
        if not table_name_validator(table_name):
            raise ValueError("Possible SQL injection attempt")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = (f"CREATE TABLE IF NOT EXISTS {table_name} (id integer PRIMARY KEY AUTOINCREMENT, "
                 f"total integer NOT NULL, "
                 f"username text NOT NULL, "
                 f"transfer integer NOT NULL, "
                 f"date_time text NOT NULL, "
                 f"description text NOT NULL);")
        cursor.execute(query)

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(str(e))

    except ValueError as e:
        print(str(e))


if __name__ == '__main__':
    pass
    # create_db()
    # create_table_group("budget_1")
