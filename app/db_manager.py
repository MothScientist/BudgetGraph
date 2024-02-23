import os
import psycopg2
from dotenv import load_dotenv
from app.logger import setup_logger
from app.encryption import get_token
from app.time_checking import timeit
import re

import time

load_dotenv()  # Load environment variables from .env file
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")
db_name = os.getenv("POSTGRES_NAME")
db_user = os.getenv("POSTGRES_USERNAME")
db_psw = os.getenv("POSTGRES_PASSWORD")

DSN = f"dbname={db_name} user={db_user} password={db_psw} host={db_host} port={db_port}"

logger_database = setup_logger("logs/DatabaseLog.log", "db_logger")


def connect_db():
    try:
        conn = psycopg2.connect(DSN)
        logger_database.debug("success: connecting to database")
        return conn

    except (psycopg2.DatabaseError, UnicodeDecodeError) as err:
        logger_database.critical(f"connecting to database: {str(err)}")


def close_db(conn):
    if conn:
        conn.close()
        logger_database.debug("success: connecting to database")


def create_db() -> None:
    """
    Creates tables, using create_db.sql file describing their structures.
    """
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            with open("create_db.sql", 'r') as file:
                cur.execute(file.read())

            conn.commit()

    except (psycopg2.DatabaseError, IOError, AttributeError) as err:
        print(f"Critical error when creating tables in the database: {err}")
        logger_database.critical(f"{err}")

    finally:
        close_db(conn)


class DatabaseQueries:
    """
    The class is used to query the database.
    All details of the structure of functions are indicated in the comments to the first function
    """
    def __init__(self, connection):
        self.__conn = connection

    def get_username_by_telegram_id(self, telegram_id: int) -> str:
        """
        :return: username | empty string
        """
        try:
            with self.__conn as conn:
                # Connections can be used as context managers.
                # Note that a context wraps a transaction:
                # if the context exits with success the transaction is committed,
                # if it exits with an exception the transaction is rolled back.
                # Note that the connection is not closed by the context, and it can be used for several contexts.
                # https://www.psycopg.org/docs/connection.html

                # TypeError occurs in this block if the database connection returned null
                with conn.cursor() as cur:
                    # Cursors can be used as context managers: leaving the context will close the cursor

                    # AttributeError occurs in this block if the database connection returned null
                    cur.execute("""SELECT username 
                                   FROM users 
                                   WHERE telegram_id = %s""", (telegram_id,))  # DO NOT REMOVE parentheses and commas
                    res = cur.fetchone()

                    if res:
                        return res[0]
                    else:
                        return ""

        except (psycopg2.DatabaseError, TypeError) as err:
            # The logs store the error and parameters that were passed to the function (except secrets)
            # The time and function where the error occurred will be added automatically
            logger_database.error(f"{str(err)}, "
                                  f"telegram_id: {telegram_id}")
            # Returning an empty string (or zero) in an exception block
            # allows validators to treat this as no data in the database
            return ""

    def get_telegram_id_by_username(self, username: str) -> int:
        """
        :return: telegram id | 0
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT telegram_id 
                                   FROM users 
                                   WHERE username = %s""", (username,))
                    res = cur.fetchone()

                    if res:
                        return res[0]
                    else:
                        return 0

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"username: {username}")
            return 0

    def get_group_id_by_token(self, token: str) -> int:
        """
        :return: group id | 0
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT id
                                   FROM groups
                                   WHERE token = %s""", (token,))
                    res = cur.fetchone()
                    if res:
                        return res[0]
                    else:
                        return 0

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"token: {token}")
            return 0

    def get_group_id_by_telegram_id(self, telegram_id: int) -> int:
        """
        :return: group id | 0.
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT group_id 
                                   FROM users 
                                   WHERE telegram_id = %s""", (telegram_id,))
                    res = cur.fetchone()

                    if res:
                        return res[0]
                    else:
                        return 0

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"telegram_id: {telegram_id}")
            return 0

    def get_group_id_by_username(self, username: str) -> int:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT group_id 
                                   FROM Users 
                                   WHERE username = %s""", (username,))
                    res = cur.fetchone()

                    if res:
                        return res[0]
                    else:
                        return 0

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"username: {username}")
            return 0

    def get_token_by_username(self, username: str) -> str:
        """
        :return: token | empty string
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT g.token
                                   FROM Groups g
                                   JOIN Users u ON g.id = u.group_id
                                   WHERE u.username = %s""", (username,))
                    res = cur.fetchone()
                    if res:
                        return res[0]
                    else:
                        return ""

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"username: {username}")
            return ""

    def get_token_by_telegram_id(self, telegram_id: int) -> str:
        """
        :return: token | empty string
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT g.token
                                   FROM Groups g
                                   JOIN Users u ON g.id = u.group_id
                                   WHERE u.telegram_id = %s""", (telegram_id,))
                    res = cur.fetchone()
                    if res:
                        return res[0]
                    else:
                        return ""

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"telegram_id: {telegram_id}")
            return ""

    def get_salt_by_username(self, username: str) -> str:
        """
        :return: salt | empty string (if this username is not in the database)
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT psw_salt 
                                   FROM Users 
                                   WHERE username = %s""", (username,))
                    res = cur.fetchone()
                    if res:
                        return str(res[0])
                    else:
                        return ""

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"username: {username}")
            return ""

    def auth_by_username(self, username: str, psw_hash: str) -> bool:
        """
        Function to confirm user authorization using three parameters
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT * 
                                   FROM Users u
                                   JOIN Groups g ON g.id = u.group_id
                                   WHERE u.username = %s
                                   AND password_hash = %s""", (username, psw_hash))
                    res = cur.fetchone()
                    if res:
                        return True
                    else:
                        return False

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"username: {username}, "
                                  f"psw_hash: {psw_hash}")
            return False

    def select_data_for_household_table(self, group_id: int, number_of_last_records: int) -> tuple:
        """
        returns the specified number of rows (starting with the most recent) from the budget table.
        :param group_id:
        :param number_of_last_records: number of rows returned.
        :return: list of n elements | empty list
        """
        table_name = f"budget_{group_id}"
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    if number_of_last_records == 0:  # getting all records
                        cur.execute(f"""SELECT *
                                        FROM {table_name}
                                        ORDER BY id DESC""")
                        res = cur.fetchall()
                    else:
                        cur.execute(f"""SELECT *
                                        FROM {table_name}
                                        ORDER BY id DESC
                                        LIMIT %s""", (number_of_last_records,))
                        res = cur.fetchall()

                    res_list: tuple[tuple, ...] = tuple(tuple(row) for row in res)
                    return res_list

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group id: {group_id}, "
                                  f"n: {number_of_last_records}, "
                                  f"table name: {table_name}")
            return ()

    def get_group_users(self, group_id: int) -> list:
        """
        :return: list (empty or with usernames of group members)
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT username
                                   FROM Users
                                   WHERE group_id = %s""", (group_id,))
                    res = cur.fetchall()
                    res_list = [str(row[0]) for row in res]
                    return res_list

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group id: {group_id}")
            return []

    def get_group_users_data(self, group_id: int) -> list:
        """
        :return: list (empty or with usernames of group members and last_login row)
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT username, last_login
                                   FROM Users
                                   WHERE group_id = %s""", (group_id,))
                    res = cur.fetchall()
                    res_list = [list(row) for row in res]
                    return res_list

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group id: {group_id}")
            return []

    def get_group_owner_username_by_group_id(self, group_id: int) -> str:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT u.username 
                                   FROM Users u 
                                   JOIN Groups g ON u.telegram_id = g.owner
                                   WHERE g.id = %s""", (group_id,))
                    res = cur.fetchone()
                    if res:
                        return str(res[0])
                    else:
                        return ""

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group id: {group_id}")
            return ""

    def check_username_is_group_owner(self, username: str, group_id: int) -> bool:
        owner_username: str = self.get_group_owner_username_by_group_id(group_id)
        if not owner_username or not username:  # check that we did not receive empty lines as input
            return False
        if owner_username == username:
            return True
        return False

    def check_record_id_is_exist(self, group_id: int, record_id: int) -> bool:
        table_name = f"budget_{group_id}"
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(f"""SELECT *
                                    FROM {table_name}
                                    WHERE id = %s""", (record_id,))
                    res = cur.fetchone()
                    if res:
                        return True
                    return False

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group id: {group_id}, "
                                  f"record id: {record_id}, "
                                  f"table name: {table_name}")
            return False

    def check_username_is_exist(self, username: str) -> bool:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT 1
                                   FROM Users
                                   WHERE username = %s""", (username,))
                    res = cur.fetchone()
                    if res:
                        return True
                    return False

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"username: {username}")
            return False

    def check_telegram_id_is_exist(self, telegram_id: int) -> bool:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT 1
                                   FROM Users
                                   WHERE telegram_id = %s""", (telegram_id,))
                    res = cur.fetchone()
                    if res:
                        return True
                    return False

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"telegram ID: {telegram_id}")
            return False

    """
    Functions for checking uniqueness are necessary to avoid problems when inserting data into a unique column
    """
    def check_token_is_unique(self, token: str) -> bool:  # necessary if you want to reduce the token length
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT *
                                   FROM Groups
                                   WHERE token = %s""", (token,))
                    res = cur.fetchone()
                    if res:
                        return False
                    else:
                        return True

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"new token: {token}")
            return False

    def check_limit_users_in_group(self, group_id: int) -> bool:
        """
        Returns: True if there are empty seats in the group.
        by token checks the group's filling limit.

        if there is no group with such a token, it will return False.
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT COUNT(telegram_id)
                                   FROM Users
                                   WHERE group_id = %s""", (group_id,))
                    res = cur.fetchone()
                    if 0 < int(res[0]) < 20:  # condition > 0 is used for secondary checking for group existence
                        return True
                    return False

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group id: {group_id}")
            return False  # to prevent a user from being written to a non-existent group

    def get_user_language(self, telegram_id) -> str:
        """
        Gets the user's (telegram_id) language from the database.
        If there is no entry for the user in the database, the default language is used.
        By default, the user will be offered text in English.
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT language
                                   FROM user_languages_telegram
                                   WHERE telegram_id = %s""", (telegram_id,))
                    res = cur.fetchone()
                    if res:
                        return str(res[0])
                    return "en"  # if the user did not change the default language

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"telegram_id: {telegram_id}")
            return "en"  # return default language

    def get_last_sum_in_group(self, group_id: int) -> int:
        """
        Gets the last total amount in the group table to then add/subtract the amount of the new transaction.
        Returns 0 if there are no records.
        """
        table_name = f"budget_{group_id}"
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(f"""SELECT total
                                    FROM {table_name}
                                    ORDER BY id DESC
                                    LIMIT 1""")
                    res = cur.fetchone()
                    if res:
                        return int(res[0])
                    return 0

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group id: {group_id}")
            return 0

    def add_user_language(self, telegram_id: int, language: str) -> bool:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""INSERT INTO user_languages_telegram (telegram_id, language)
                                   VALUES (%s, %s)
                                   ON CONFLICT (telegram_id) 
                                   DO UPDATE SET language = %s""", (telegram_id, language, language))
                    conn.commit()

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"telegram_id: {telegram_id}, "
                                  f"language: {language}")
            return False

        else:
            return True

    def add_user_to_db(self, username: str, psw_salt: str, psw_hash: str, group_id: int, telegram_id: int) -> bool:
        """
        Insert a new user to the Users table
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""INSERT INTO Users (telegram_id, username, psw_salt, psw_hash, group_id, last_login)
                                   VALUES(%s, %s, %s, %s, %s, 
                                   to_char(current_timestamp AT TIME ZONE 'UTC', 'DD/MM/YYYY HH24:MI:SS'))""",
                                   (telegram_id, username, psw_salt, psw_hash, group_id,))
                    # to_char is required to change the date-time format
                    conn.commit()

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"username: {username}, "
                                  f"psw_salt: {psw_salt}, "
                                  f"psw_hash: {psw_hash}, "
                                  f"group_id: {group_id}, "
                                  f"telegram_id: {telegram_id}")
            return False

        else:
            return True

    @timeit
    def add_monetary_transaction_to_db(self, username: str, group_id: int, value: int, last_total_sum: int, record_date: str, category: str, description: str) -> bool:  # noqa (E501)
        """
        submits the "add_expense" and "add_income" forms to the database.
        :param username: the name of the user is making the changes.
        :param group_id:
        :param value: value of the deposited amount (can be both negative and positive)
        :param last_total_sum: last 'total' value in the table (can be both negative and positive)
        :param category:  # TODO сделать тоже необязательным параметром (как и description)
        :param description: optional parameter
        :param record_date:
        """
        table_name = f"budget_{group_id}"
        total_sum: int = last_total_sum + value
        # In the table must be entered with the user's name in the text format because the user can later be deleted,
        # but their entries must remain in the table until it is deleted or cleared by the group owner.
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:  # TODO тут дату нашего формата надо пометить как date внутри postgres
                    cur.execute(f"""INSERT INTO {table_name} (total, username, transfer, category, record_date, description)
                                    VALUES (%s, %s,%s, %s, %s, %s)""",  # noqa (E501)
                                    (total_sum, username, value, category, record_date, description))
                    conn.commit()
        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group id: {group_id}, "
                                  f"table name: {table_name}, "
                                  f"username: {username}, "
                                  f"value: {value}, "
                                  f"description: {description}")
            return False

        else:
            return True

    def create_new_group(self, owner: int) -> str:  # TODO что-то сделать с проверкой токена - выносить за функцию
        """
        creating a new group in the Groups table and generate a new token for this group.
        :param owner: link to the telegram of the user who initiates the creation of the group.
        :return: token | empty string
        """
        token = get_token()
        token_is_unique: bool = self.check_token_is_unique(token)

        while not token_is_unique:  # checking the token for uniqueness
            token = get_token()
            token_is_unique = self.check_token_is_unique(token)

        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""INSERT INTO Groups (owner, token)
                                          VALUES(%s, %s)""", (owner, token,))
                    conn.commit()

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"owner (telegram id): {owner}")
            return ""

        else:
            return token

# Methods for updating data in a database (UPDATE)

    def update_user_last_login_by_telegram_id(self, telegram_id: int) -> None:
        """
        Changes the user's last login time in the last_login column in the Users table.
        :return: None
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""UPDATE users 
                                   SET last_login = to_char(current_timestamp AT TIME ZONE 'UTC', 'DD/MM/YYYY HH24:MI:SS')
                                   WHERE telegram_id = %s""", (telegram_id,))  # noqa: E501
                    conn.commit()

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"telegram_id: {telegram_id}")

    def update_user_last_login_by_username(self, username: str) -> None:
        """
        Changes the user's last login time in the last_login column in the Users table.
        :return: None
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""UPDATE users 
                                   SET last_login = to_char(current_timestamp AT TIME ZONE 'UTC', 'DD/MM/YYYY HH24:MI:SS')
                                   WHERE username = %s""", (username,))  # noqa: E501
                    conn.commit()

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"username: {username}")

    def update_group_owner(self, telegram_id: int, group_id: int) -> bool:
        """
        Changes the owner of a group to another user from that group
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""UPDATE groups 
                                   SET owner = %s 
                                   WHERE id = %s""", (telegram_id, group_id,))
                    conn.commit()
                    return True

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"telegram_id: {telegram_id}, "
                                  f"group_id: {group_id}")
            return False

# Methods for deleting database data (DELETE)

    def delete_budget_entry_by_id(self, group_id: int, record_id: int) -> bool:
        """
        Removes an entry from the group budget table.
        :param group_id:
        :param record_id: Row id in the table
        :return: True - if the entry is found and successfully deleted, else - False
        """
        table_name = f"budget_{group_id}"
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(f"""DELETE FROM {table_name} 
                                    WHERE id = %s""", (record_id,))
                    conn.commit()

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group id: {group_id}, "
                                  f"record id: {record_id}, "
                                  f"table name: {table_name}")
            return False

        else:
            return True

    def update_total_sum_after_delete_record(self, transaction: int, record_id: int) -> bool:
        pass  # TODO

    def delete_username_from_users(self, username: str) -> bool:
        """
        Removes a user from a group (not the owner)
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""DELETE FROM users 
                                   WHERE username = %s""", (username,))
                    conn.commit()

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"username: {username}")
            return False

        else:
            logger_database.info(f"User '{username}' has been removed from the database")
            return True

    def delete_group_with_users(self, group_id: int) -> bool:  # TODO REFERENCES IN .sql
        """
        Deletes the group table along with all its members (including the owner)
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""DELETE FROM users 
                                   WHERE group_id = %s""", (group_id,))

                    cur.execute("""DELETE FROM groups 
                                   WHERE id = %s""", (group_id,))

                    cur.execute(f"""DROP TABLE budget_{group_id}""")
                    conn.commit()

        except (psycopg2.DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group id: {group_id}")
            return False

        else:
            logger_database.info(f"Group #{group_id} has been completely deleted")
            return True


def create_table_group(table_name: str) -> None:  # TODO вынести валидацию
    """  # TODO но вообще нужно отказаться от концепции динамического создания таблиц
    creates a table in the database called budget_?
    (id, total, username, transfer, date_time, description)

    contains table_name_validator -> to protect against sql injection, validation of the table_name parameter is needed
    :param table_name: "budget_?"
    """
    try:  # TODO делать проверку категории
        if not re.match(r"^budget_[1-9]\d{0,4}$", table_name):
            raise ValueError("Possible SQL injection attempt")
        conn = connect_db()
        with conn:
            with conn.cursor() as cur:  # TODO date format
                query = (f"""CREATE TABLE IF NOT EXISTS {table_name}
                             (id SERIAL PRIMARY KEY,
                             total integer NOT NULL,
                             username varchar(20) NOT NULL,
                             transfer integer NOT NULL,
                             category varchar(25) NOT NULL,
                             record_date text NOT NULL,
                             description text NOT NULL CHECK(LENGTH(description) <= 50));""")
                cur.execute(query)
                conn.commit()

    except (psycopg2.DatabaseError, TypeError) as err:
        logger_database.error(f"{str(err)}, Table name: {table_name}")

    except ValueError as err:
        logger_database.error(f"{str(err)}, Value (table name): {table_name}")

    else:
        logger_database.info(f"Successful table creation: {table_name}")
