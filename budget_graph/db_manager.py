import os
from psycopg2 import connect, DatabaseError
from dotenv import load_dotenv
from flask import g

from budget_graph.logger import setup_logger
from budget_graph.encryption import get_token, logging_hash
from budget_graph.time_checking import timeit

load_dotenv()  # Load environment variables from .env file
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")
db_name = os.getenv("POSTGRES_NAME")
db_user = os.getenv("POSTGRES_USERNAME")
db_psw = os.getenv("POSTGRES_PASSWORD")

DSN = f"dbname={db_name} user={db_user} password={db_psw} host={db_host} port={db_port}"

logger_database = setup_logger("logs/DatabaseLog.log", "db_logger")


@timeit
def connect_db():
    try:
        conn = connect(DSN)
        logger_database.debug("SUCCESS: connecting to database")
        return conn
    except (DatabaseError, UnicodeDecodeError) as err:
        logger_database.critical(f"connecting to database: {str(err)}")


def close_db(conn):
    if conn:
        conn.close()
        logger_database.debug("SUCCESS: connection to database closed")


def connect_db_flask_g():
    """
    connect to a database using a Flask application object.
    :return: connection
    """
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db


def close_db_flask_g(error):  # DO NOT REMOVE the parameter  # noqa
    """
    Closing a database connection using a Flask application object.
    """
    if hasattr(g, "link_db"):
        g.link_db.close()


class DatabaseQueries:
    """
    The class is used to query the database.
    All details of the structure of functions are indicated in the comments to the first function
    """
    def __init__(self, connection):
        self.__conn = connection

    @timeit
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
                    cur.execute("""SELECT "username"
                                   FROM "budget_graph"."users"
                                   WHERE "telegram_id" = %s""", (telegram_id,))  # DO NOT REMOVE commas
                    res = cur.fetchone()
                    if res:
                        return res[0]
                    return ''

        except (DatabaseError, TypeError) as err:
            # The logs store the error and parameters that were passed to the function (except secrets)
            # The time and function where the error occurred will be added automatically
            logger_database.error(f"{str(err)}, "
                                  f"telegram_id: {logging_hash(telegram_id)}")
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
                    cur.execute("""SELECT "telegram_id"
                                   FROM "budget_graph"."users"
                                   WHERE "username" = %s""", (username,))
                    res = cur.fetchone()

                    if res:
                        return res[0]
                    return 0
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"username: {logging_hash(username)}")
            return 0

    def get_group_id_by_token(self, token: str) -> int:
        """
        :return: group id | 0
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT "id"
                                   FROM "budget_graph"."groups"
                                   WHERE "token" = %s""", (token,))
                    res = cur.fetchone()
                    if res:
                        return res[0]
                    return 0
        except (DatabaseError, TypeError) as err:
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
                    cur.execute("""SELECT "group_id"
                                   FROM "budget_graph"."users"
                                   WHERE "telegram_id" = %s""", (telegram_id,))
                    res = cur.fetchone()

                    if res:
                        return res[0]
                    return 0
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"telegram_id: {logging_hash(telegram_id)}")
            return 0

    def get_token_by_username(self, username: str) -> str:
        """
        :return: token | empty string
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT g."token"
                                   FROM "budget_graph"."groups" g
                                   JOIN "budget_graph"."users" u
                                   ON g.id = u."group_id"
                                   WHERE u."username" = %s""", (username,))
                    res = cur.fetchone()
                    if res:
                        return res[0]
                    return ''
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"username: {logging_hash(username)}")
            return ''

    def get_token_by_telegram_id(self, telegram_id: int) -> str:
        """
        :return: token | empty string
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT g."token"
                                   FROM "budget_graph"."groups" g
                                   JOIN "budget_graph"."users" u
                                   ON g."id" = u."group_id"
                                   WHERE u."telegram_id" = %s""", (telegram_id,))
                    res = cur.fetchone()
                    if res:
                        return res[0]
                    return ""
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"telegram_id: {logging_hash(telegram_id)}")
            return ""

    def get_salt_by_username(self, username: str) -> str:
        """
        :return: salt | empty string (if this username is not in the database)
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT "psw_salt"
                                   FROM "budget_graph"."users"
                                   WHERE "username" = %s""", (username,))
                    res = cur.fetchone()
                    if res:
                        return str(res[0])
                    return ""
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"username: {logging_hash(username)}")
            return ""

    def auth_by_username(self, username: str, psw_hash: str) -> bool:
        """
        Function to confirm user authorization using three parameters
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT 1
                                   FROM "budget_graph"."users" u
                                   JOIN "budget_graph"."groups" g
                                   ON g."id" = u."group_id"
                                   WHERE u."username" = %s
                                   AND u."psw_hash" = %s""", (username, psw_hash))
                    res = cur.fetchone()
                    if res:
                        return True
                    return False
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"username: {logging_hash(username)}")
            return False

    def select_data_for_household_table(self, group_id: int, number_of_last_records: int) -> tuple:
        """
        Returns the specified number of rows (starting with the most recent)
        from monetary_transactions table.
        :param group_id:
        :param number_of_last_records: number of rows returned.
        :return: tuple of n elements | empty list
        """
        # add a restriction on overload protection
        # when requesting all data from the table
        number_of_last_records = 10_000 if number_of_last_records == 0 else number_of_last_records
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    # getting all records (max 10.000)
                    if number_of_last_records == 0:
                        # use ASC
                        cur.execute("""
                                       SELECT
                                            "transaction_id",
                                            "username",
                                            "transfer",
                                            "total",
                                            to_char("record_date", 'DD/MM/YYYY') as record_date,
                                            "category",
                                            "description"
                                       FROM "budget_graph"."monetary_transactions"
                                       WHERE "group_id" = %s
                                       ORDER BY "transaction_id" ASC
                                       LIMIT %s""",
                                    (group_id, number_of_last_records,))
                        res = cur.fetchall()
                    else:
                        # use DESC to make it easier for the user to read
                        cur.execute(f"""
                                        SELECT 
                                            "transaction_id",
                                            "username",
                                            "transfer",
                                            "total",
                                            "to_char"("record_date", 'DD/MM/YYYY') as record_date,
                                            "category",
                                            "description"
                                        FROM "budget_graph"."monetary_transactions"
                                        WHERE "group_id" = %s
                                        ORDER BY "transaction_id" DESC
                                        LIMIT %s""",
                                    (group_id, number_of_last_records,))
                        res = cur.fetchall()

                    res_list: tuple[tuple, ...] = tuple(tuple(row) for row in res)
                    return res_list
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group id: {group_id}, "
                                  f"n: {number_of_last_records}")
            return ()

    def get_group_users(self, group_id: int) -> tuple:
        """
        :return: list (empty or with usernames of group members)
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT "username"
                                   FROM "budget_graph"."users"
                                   WHERE "group_id" = %s""", (group_id,))
                    res = cur.fetchall()
                    res_list = tuple(str(row[0]) for row in res)
                    return res_list
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group id: {group_id}")
            return ()

    def get_group_users_data(self, group_id: int) -> list:
        """
        :return: list (empty or with usernames of group members and last_login row)
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT "username", "last_login"
                                   FROM "budget_graph"."users"
                                   WHERE "group_id" = %s""", (group_id,))
                    res = cur.fetchall()
                    res_list = [list(row) for row in res]
                    return res_list
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group id: {group_id}")
            return []

    def get_group_owner_telegram_id_by_group_id(self, group_id: int) -> int:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT "owner"
                                   FROM "budget_graph"."groups"
                                   WHERE "id" = %s""", (group_id,))
                    res = cur.fetchone()
                    if res:
                        return res[0]
                    return 0
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group id: {group_id}")
            return 0

    def check_user_is_group_owner_by_telegram_id(self, telegram_id: int, group_id: int) -> bool:
        owner_telegram_id: int = self.get_group_owner_telegram_id_by_group_id(group_id)
        if not owner_telegram_id or not telegram_id:  # check that we did not receive empty lines as input
            return False
        if owner_telegram_id == telegram_id:  # TODO security
            return True
        return False

    def get_group_owner_username_by_group_id(self, group_id: int) -> str:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT u."username"
                                   FROM "budget_graph"."users" u
                                   JOIN "budget_graph"."groups" g
                                   ON u."telegram_id" = g."owner"
                                   WHERE g."id" = %s""", (group_id,))
                    res = cur.fetchone()
                    if res:
                        return str(res[0])
                    return ""
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group id: {group_id}")
            return ""

    def check_record_id_is_exist(self, group_id: int, transaction_id: int) -> bool:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(f"""SELECT 1
                                    FROM "budget_graph"."monetary_transactions"
                                    WHERE "group_id" = %s
                                    AND "transaction_id" = %s""", (group_id, transaction_id,))
                    res = cur.fetchone()
                    if res:
                        return True
                    return False
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group ID: {group_id}, "
                                  f"transaction ID: {transaction_id}")
            return False

    def check_username_is_exist(self, username: str) -> bool:
        """
        The name is unique and case independent, i.e. you cannot create 'John' and 'john' -> only one of them
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT 1
                                   FROM "budget_graph"."users"
                                   WHERE LOWER("username") = LOWER(%s)""", (username,))
                    res = cur.fetchone()
                    if res:
                        return True
                    return False

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"username: {logging_hash(username)}")
            return False

    def check_telegram_id_is_exist(self, telegram_id: int) -> bool:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT 1
                                   FROM "budget_graph"."users"
                                   WHERE "telegram_id" = %s""", (telegram_id,))
                    res = cur.fetchone()
                    if res:
                        return True
                    return False
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"telegram ID: {logging_hash(telegram_id)}")
            return False

    def check_token_is_unique(self, token: str) -> bool:
        """
        Checking the uniqueness of the generated token to avoid problems when inserting data into a unique column.
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT 1
                                   FROM "budget_graph"."groups"
                                   WHERE "token" = %s""", (token,))
                    res = cur.fetchone()
                    if res:
                        return False
                    return True

        except (DatabaseError, TypeError) as err:
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
                    cur.execute("""SELECT COUNT(*)
                                   FROM "budget_graph"."users"
                                   WHERE "group_id" = %s""", (group_id,))
                    res = cur.fetchone()
                    if 0 < int(res[0]) < 20:  # condition > 0 is used for secondary checking for group existence
                        return True
                    return False
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group id: {group_id}")
            return False  # to prevent a user from being written to a non-existent group

    @timeit
    def get_user_language(self, telegram_id: int) -> str:
        """
        Gets the user's (telegram_id) language from the database.
        If there is no entry for the user in the database, the default language is used.
        By default, the user will be offered text in English.
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT "language"
                                   FROM "budget_graph"."user_languages_telegram"
                                   WHERE "telegram_id" = %s""", (telegram_id,))
                    res = cur.fetchone()
                    if res:
                        return str(res[0])
                    return "en"  # if the user did not change the default language

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"telegram_id: {logging_hash(telegram_id)}")
            return "en"  # return default language

    def add_user_language(self, telegram_id: int, language: str) -> bool:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                                   INSERT INTO "budget_graph"."user_languages_telegram"
                                   ("telegram_id", "language")
                                   VALUES (%s, %s)
                                   ON CONFLICT ("telegram_id")
                                   DO UPDATE SET "language" = %s
                                """, (telegram_id, language, language))
                    conn.commit()
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"telegram_id: {logging_hash(telegram_id)}, "
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
                    cur.execute("""
                                   INSERT INTO "budget_graph"."users"
                                   ("telegram_id", "username", "psw_salt", "psw_hash", "group_id", "last_login")
                                   VALUES(%s, %s, %s, %s, %s,
                                   to_char(current_timestamp AT TIME ZONE 'UTC', 'DD/MM/YYYY HH24:MI:SS'))
                                """, (telegram_id, username, psw_salt, psw_hash, group_id,))
                    # to_char is required to change the date-time format
                    conn.commit()
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"username: {logging_hash(username)}, "
                                  f"group_id: {group_id}, "
                                  f"telegram_id: {logging_hash(telegram_id)}")
            return False
        else:
            return True

    @timeit
    def add_transaction_to_db(self,
                              username: str,
                              transaction_amount: int,
                              record_date: str,
                              category: str,
                              description: str) -> bool:
        """
        The function records user transactions in the database.

        :param username: username of the user is making the transaction.
        :param transaction_amount: value of the deposited amount (can be both negative and positive)
        :param category:
        :param description:
        :param record_date:
        """
        telegram_id: int = self.get_telegram_id_by_username(username)
        group_id: int = self.get_group_id_by_telegram_id(telegram_id)
        last_total_sum: int = self.get_last_sum_in_group(group_id)
        total_sum: int = last_total_sum + transaction_amount
        transaction_id: int = self.get_last_transaction_id_in_group(group_id) + 1
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(f"""
                                    INSERT INTO "budget_graph"."monetary_transactions"
                                    ("group_id", "transaction_id", "username", "total",
                                    "transfer", "record_date", "category", "description")
                                    VALUES (%s, %s,%s, %s, %s, %s, %s, %s)
                                 """, (group_id, transaction_id,
                                       username, total_sum, transaction_amount,
                                       record_date, category, description))
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group id: {group_id}, "
                                  f"transaction_id: {transaction_id}"
                                  f"username: {logging_hash(username)}, "
                                  f"total_sum: {total_sum}, "
                                  f"transaction_amount: {transaction_amount},"
                                  f"record_date: {record_date},"
                                  f"category: {category},"
                                  f"description: {description}")
            return False
        else:
            return True

    def get_last_sum_in_group(self, group_id: int) -> int:
        """
        Gets the last 'total' amount in table by group ID.
        Returns 0 if there are no records.
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT "total"
                                   FROM "budget_graph"."monetary_transactions"
                                   WHERE "group_id" = %s
                                   ORDER BY "transaction_id" DESC
                                   LIMIT 1""", (group_id,))
                    res = cur.fetchone()
                    if res:
                        return int(res[0])
                    return 0
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group id: {group_id}")
            return 0

    def get_last_transaction_id_in_group(self, group_id: int) -> int:
        """
        Gets the ID of the last transaction in the table by group ID.
        Returns 0 if there are no entries.
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""SELECT "transaction_id"
                                   FROM "budget_graph"."monetary_transactions"
                                   WHERE "group_id" = %s
                                   ORDER BY "transaction_id" DESC
                                   LIMIT 1""", (group_id,))
                    res = cur.fetchone()
                    if res:
                        return int(res[0])
                    return 0

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group id: {group_id}")
            return 0

    def get_group_transfer_by_transaction_id(self, group_id: int, transaction_id: int) -> int:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                                   SELECT "transfer"
                                   FROM "budget_graph"."monetary_transactions"
                                   WHERE "group_id" = %s AND "transaction_id" = %s
                                """, (group_id, transaction_id,))
                    res = cur.fetchone()
                    if res:
                        return int(res[0])
                    return 0
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group id: {group_id},"
                                  f"transaction_id: {transaction_id}")
            return 0

    def process_delete_transaction_record(self, group_id: int, transaction_id: int) -> bool:
        """
        Calls 3 functions in sequence, which:
        1. Receive the amount of this transaction - Gets the value of the 'transfer' field
        based on the group's transaction ID.
        2. Adjust subsequent transactions - Recalculation of 'total' fields that come after the deleted field.
        3. Delete the required entry - Removes a record from a group transaction.
        """
        # Getting the value 'transfer' in the field being deleted
        difference_transfer: int = self.get_group_transfer_by_transaction_id(group_id, transaction_id)
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    # Correction of the 'total' field in all records following the one being deleted
                    cur.execute("""UPDATE "budget_graph"."monetary_transactions"
                                   SET "total" = "total" - %s
                                   WHERE "group_id" = %s AND "transaction_id" > %s""",
                                   (difference_transfer, group_id, transaction_id,))

                    # Delete transaction record
                    cur.execute("""DELETE
                                   FROM "budget_graph"."monetary_transactions"
                                   WHERE "group_id" = %s AND "transaction_id" = %s""",
                                   (group_id, transaction_id,))
                    conn.commit()
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group ID: {group_id}, "
                                  f"transaction ID: {transaction_id}")
            return False
        else:
            return True

    def create_new_group(self, owner: int) -> str:  # TODO do something with token verification - make it a function
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
                    cur.execute("""
                                   INSERT INTO "budget_graph"."groups"
                                   ("owner", "token")
                                   VALUES(%s, %s)
                                """, (owner, token,))
                    conn.commit()
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"owner (telegram id): {logging_hash(owner)}")
            return ""
        else:
            return token

    def update_user_last_login_by_telegram_id(self, telegram_id: int) -> None:
        """
        Changes the user's last login time in the last_login column in the Users table.
        :return: None
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""UPDATE "budget_graph"."users"
                                   SET "last_login" = to_char(current_timestamp AT TIME ZONE 'UTC', 'DD/MM/YYYY HH24:MI:SS')
                                   WHERE "telegram_id" = %s""", (telegram_id,))  # noqa: E501
                    conn.commit()
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"telegram_id: {logging_hash(telegram_id)}")

    def update_group_owner(self, telegram_id: int, group_id: int) -> bool:
        """
        Changes the owner of a group to another user from that group
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""UPDATE "budget_graph"."groups"
                                   SET "owner" = %s
                                   WHERE "id" = %s""", (telegram_id, group_id,))
                    conn.commit()
                    return True
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"telegram_id: {logging_hash(telegram_id)}, "
                                  f"group_id: {group_id}")
            return False

    def delete_username_from_users_by_telegram_id(self, telegram_id: int) -> bool:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""DELETE FROM "budget_graph"."users"
                                   WHERE "telegram_id" = %s""", (telegram_id,))
                    conn.commit()
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"telegram ID: {logging_hash(telegram_id)}")
            return False
        else:
            logger_database.info(f"Telegram ID {logging_hash(telegram_id)} has been removed from the database")
            return True

    def delete_group_with_users(self, group_id: int) -> bool:  # TODO REFERENCES IN .sql
        """
        Deletes the group table along with all its members (including the owner)
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""DELETE FROM "budget_graph"."users"
                                   WHERE "group_id" = %s""", (group_id,))

                    cur.execute("""DELETE FROM "budget_graph"."groups"
                                   WHERE "id" = %s""", (group_id,))

                    cur.execute("""DELETE FROM "budget_graph"."monetary_transactions"
                                   WHERE "group_id" = %s""", (group_id,))

                    conn.commit()
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"{str(err)}, "
                                  f"group ID: {group_id}")
            return False
        else:
            logger_database.info(f"Group #{group_id} has been completely deleted")
            return True
