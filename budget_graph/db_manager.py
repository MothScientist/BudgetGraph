from datetime import datetime
from os import getenv, path
from functools import wraps
from flask import g
from dotenv import load_dotenv
from psycopg2 import connect, DatabaseError

from budget_graph.logger import setup_logger
from budget_graph.time_checking import timeit
from budget_graph.encryption import get_token, logging_hash

load_dotenv()  # Load environment variables from .env file
db_host = getenv('POSTGRES_HOST')
db_port = getenv('POSTGRES_PORT')
db_name = getenv('POSTGRES_NAME')
db_user = getenv('POSTGRES_USERNAME')
db_psw = getenv('POSTGRES_PASSWORD')

DSN = f'dbname={db_name} user={db_user} password={db_psw} host={db_host} port={db_port}'

logger_database = setup_logger('logs/DatabaseLog.log', 'db_logger')


@timeit
def connect_db():
    try:
        conn = connect(DSN)
    except (DatabaseError, UnicodeDecodeError) as err:
        logger_database.critical(f'[DB_CONNECT] FAILED: connecting to database: {str(err)}')
        return None

    logger_database.debug('[DB_CONNECT] SUCCESS: connecting to database')
    return conn


def close_db(conn):
    if conn:
        conn.close()
        logger_database.debug('[DB_CONNECT] SUCCESS: connection to database closed')


def connect_defer_close_db(func):
    """
    This function is used as a decorator that creates a connection to the database,
    passes a pointer and closes the connection after execution

    :return: db_connection -> object of the DatabaseQueries class used to call the class functions
    """
    # @wraps is used to preserve the metadata of the original function when it is wrapped by another decorator
    # pylint: disable=inconsistent-return-statements
    @wraps(func)
    def wrapper(*args, **kwargs):
        connection = None
        try:
            res = DatabaseQueries(connect_db())
            logger_database.debug("[DB_CONNECT][defer] SUCCESS: db query was processed using the 'defer' decorator")
            return func(res, *args, **kwargs)
        # pylint: disable=broad-exception-raised
        except Exception as err:
            # all the necessary event handlers are already contained inside the called functions
            logger_database.debug(f'[DB_CONNECT][defer] FAILED: connecting to database: {str(err)}')
        finally:
            # logging is inside the function
            close_db(connection)  # the 'if' condition is not required since it is inside the called function
    return wrapper


def connect_db_flask_g():
    """
    connect to a database using a Flask application object.
    :return: connection
    """
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


# pylint: disable=unused-argument
def close_db_flask_g(error):  # DO NOT REMOVE the parameter  # noqa
    """
    Closing a database connection using a Flask application object.
    """
    if hasattr(g, 'link_db'):
        g.link_db.close()


def read_sql_file(request_name):
    filename: str = path.join(path.dirname(__file__), f'sql/{request_name}.sql')
    logger_database.info(f'[DB_QUERY] request to *.sql file: {filename}')
    with open(filename, 'r', encoding='utf-8') as sql_file:
        return sql_file.read()


# pylint: disable=too-many-public-methods
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
                    cur.execute(read_sql_file('get_username_by_telegram_id'), {'telegram_id': telegram_id})
                    return res[0] if (res := cur.fetchone()) else ''

        except (DatabaseError, TypeError) as err:
            # The logs store the error and parameters that were passed to the function (except secrets)
            # The time and function where the error occurred will be added automatically
            logger_database.error(f"[DB_QUERY] {str(err)}, "
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
                    cur.execute(read_sql_file('get_telegram_id_by_username'), {'username': username})
                    return res[0] if (res := cur.fetchone()) else 0

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"username: {logging_hash(username)}")
            return 0

    def get_group_id_by_token(self, token: str) -> int:
        """
        :return: group id | 0
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('get_group_id_by_token'), {'token': token})
                    return res[0] if (res := cur.fetchone()) else 0

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"token: {token}")
            return 0

    def get_group_id_by_telegram_id(self, telegram_id: int) -> int:
        """
        :return: group id | 0.
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('get_group_id_by_telegram_id'), {'telegram_id': telegram_id})
                    return res[0] if (res := cur.fetchone()) else 0

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"telegram_id: {logging_hash(telegram_id)}")
            return 0

    def get_group_id_token_by_username(self, username: str) -> tuple[str, int]:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('get_group_id_token_by_username'), {'username': username})
                    return res[0] if (res := cur.fetchall()) else ('', 0)

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"username: {logging_hash(username)}")
            return '', 0

    def get_token_by_telegram_id(self, telegram_id: int) -> str:
        """
        :return: token | empty string
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('get_token_by_telegram_id'), {'telegram_id': telegram_id})
                    return res[0] if (res := cur.fetchone()) else ''

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"telegram_id: {logging_hash(telegram_id)}")
            return ""

    def get_salt_by_username(self, username: str) -> str:
        """
        :return: salt | empty string (if this username is not in the database)
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('get_salt_by_username'), {'username': username})
                    return res[0] if (res := cur.fetchone()) else ''

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"username: {logging_hash(username)}")
            return ''

    def auth_by_username(self, username: str, psw_hash: str) -> bool:
        """
        Function to confirm user authorization using three parameters
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('auth_by_username'), {'username': username, 'psw_hash': psw_hash})
                    return bool(cur.fetchone()[0])

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"username: {logging_hash(username)}")
            return False

    def select_data_for_household_table(self, group_id: int, number_of_last_records: int) -> tuple[tuple, ...]:
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
                        cur.execute("""SELECT
                                         "transaction_id",
                                         "username",
                                         "transfer",
                                         "total",
                                         to_char("record_date", 'DD/MM/YYYY')::date record_date,
                                         "category",
                                         "description"
                                       FROM
                                         "budget_graph"."monetary_transactions"
                                       WHERE
                                         "group_id" = %s::smallint
                                       ORDER BY
                                         "record_date" ASC,
                                         "transaction_id" ASC
                                       LIMIT
                                         %s::smallint""",
                                    (group_id, number_of_last_records,))
                    else:
                        # use DESC to make it easier for the user to read
                        cur.execute("""SELECT
                                         "transaction_id",
                                         "username",
                                         "transfer",
                                         "total",
                                         "to_char"("record_date", 'DD/MM/YYYY')::date record_date,
                                         "category",
                                         "description"
                                       FROM
                                         "budget_graph"."monetary_transactions"
                                       WHERE
                                         "group_id" = %s::smallint
                                       ORDER BY
                                         "record_date" DESC,
                                         "transaction_id" DESC
                                       LIMIT
                                         %s::smallint""",
                                    (group_id, number_of_last_records,))
                    return tuple(tuple(row) for row in cur.fetchall())

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"group id: {group_id}, "
                                  f"n: {number_of_last_records}")
            return ()

    def get_group_usernames(self, group_id: int) -> tuple:
        """
        :return: tuple (empty or with usernames of group members)
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('get_group_usernames'), {'group_id': group_id})
                    return tuple(str(row[0]) for row in cur.fetchall())

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"group id: {group_id}")
            return ()

    def get_group_telegram_ids(self, group_id: int) -> tuple:
        """
        :return: tuple (empty or with telegram_ids of group members)
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('get_group_telegram_ids'), {'group_id': group_id})
                    return tuple(row[0] for row in cur.fetchall())

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"group id: {group_id}")
            return ()

    def get_group_transaction_uuid(self, group_id: int) -> str:
        """
        :return: transaction uuid
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('get_group_transaction_uuid'), {'group_id': group_id})
                    return cur.fetchone()[0]

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"group id: {group_id}")
            return ''

    def get_group_users_data(self, group_id: int) -> list:
        """
        :return: list (empty or with usernames of group members and last_login row)
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('get_group_users_data'), {'group_id': group_id})
                    return [list(row) for row in cur.fetchall()]

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"group id: {group_id}")
            return []

    def check_user_is_group_owner_by_telegram_id(self, telegram_id: int, group_id: int) -> bool:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        read_sql_file('check_user_is_group_owner_by_telegram_id'),
                        {'owner': telegram_id, 'group_id': group_id}
                    )
                    return bool(cur.fetchone()[0])

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"telegram_id: {logging_hash(telegram_id)}"
                                  f"group id: {group_id}")
            return False

    def get_group_owner_username_by_group_id(self, group_id: int) -> str:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('get_group_owner_username_by_group_id'), {'group_id': group_id})
                    return res[0] if (res := cur.fetchone()) else ''

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"group id: {group_id}")
            return ''

    def get_data_for_plot_builder(
            self,
            telegram_id: int,
            diagram_type: int,
            dates: list | tuple = tuple([None, None])
    ) -> dict[str, tuple]:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('get_data_for_plot_builder'), {
                        'telegram_id': telegram_id, 'diagram_type': diagram_type,
                        'start_date': dates[0], 'end_date': dates[1]
                    })
                    return {item[0]: (item[1], item[2]) for item in cur.fetchall()}

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"telegram_id: {telegram_id}, diagram_type: {diagram_type}, "
                                  f"dates: {dates}, start_date: {dates[0]}, end_date: {dates[1]}")
            return {}

    def get_group_owner_telegram_id_by_group_id(self, group_id: int) -> int:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('get_group_owner_telegram_id_by_group_id'), {'group_id': group_id})
                    return res[0] if (res := cur.fetchone()) else 0

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"group id: {group_id}")
            return 0

    def get_user_timezone_by_telegram_id(self, telegram_id: int) -> int | None:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('get_user_timezone_by_telegram_id'), {'telegram_id': telegram_id})
                    return cur.fetchone()[0]

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"group id: {telegram_id}")
            return None

    def check_record_id_is_exist(self, group_id: int, transaction_id: int) -> bool:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('check_record_id_is_exist'),
                                {'group_id': group_id, 'transaction_id': transaction_id})
                    return bool(cur.fetchone()[0])

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
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
                    cur.execute(read_sql_file('check_username_is_exist'), {'username': username})
                    return bool(cur.fetchone()[0])

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"username: {logging_hash(username)}")
            return False

    def check_telegram_id_is_exist(self, telegram_id: int) -> bool:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('check_telegram_id_is_exist'), {'telegram_id': telegram_id})
                    return bool(cur.fetchone()[0])

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"telegram ID: {logging_hash(telegram_id)}")
            return False

    def check_token_is_unique(self, token: str) -> bool:
        """
        Checking the uniqueness of the generated token to avoid problems when inserting data into a unique column.
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('check_token_is_unique'), {'token': token})
                    return not bool(cur.fetchone()[0])

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
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
                    cur.execute(read_sql_file('check_limit_users_in_group'), {'group_id': group_id})
                    return bool(cur.fetchone()[0])

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"group id: {group_id}")
            return False  # to prevent a user from being written to a non-existent group

    def get_feature_status_del_msg_after_transaction(self, telegram_id: int) -> bool:
        """
        Checks the status whether the function is enabled
        for the operation of the StorageMsgIdForDeleteAfterOperation class
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        read_sql_file('get_feature_status_del_msg_after_transaction'),
                        {'telegram_id': telegram_id}
                    )
                    return bool(cur.fetchone()[0])

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"telegram_id: {telegram_id}")
            return False  # default value - False

    def change_feature_status_del_msg_after_transaction(self, telegram_id: int) -> bool:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        read_sql_file('change_feature_status_del_msg_after_transaction'),
                        {'telegram_id': telegram_id}
                    )
                    conn.commit()
            logger_database.info(f"[del_msg_transaction] successfully changed for {logging_hash(telegram_id)}")
            return True

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"telegram_id: {telegram_id}")
            return False

    def get_user_language(self, telegram_id: int) -> str:
        """
        Gets the user's (telegram_id) language from the database.
        If there is no entry for the user in the database, the default language is used.
        By default, the user will be offered text in English.
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('get_user_language'), {'telegram_id': telegram_id})
                    # if the user did not change the default language
                    return res[0] if (res := cur.fetchone()) else 'en'

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"telegram_id: {logging_hash(telegram_id)}")
            return 'en'  # return default language

    def add_user_language(self, telegram_id: int, language: str) -> bool:  # TODO - мне кажется можно проще и яснее
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""INSERT INTO
                                     "budget_graph"."user_languages_telegram"
                                     ("telegram_id", "language")
                                   VALUES
                                     (%s, %s)
                                   ON CONFLICT
                                     ("telegram_id")
                                   DO UPDATE SET
                                     "language" = %s::text""", (telegram_id, language, language))
                    conn.commit()
                    return True

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"telegram_id: {logging_hash(telegram_id)}, "
                                  f"language: {language}")
            return False

    def add_user_timezone(self, telegram_id: int, timezone: int) -> bool:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('add_user_timezone'), {'timezone': timezone, 'telegram_id': telegram_id})
                    conn.commit()
                    return True

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"telegram_id: {logging_hash(telegram_id)}, "
                                  f"timezone: {timezone}")
            return False

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def add_transaction_to_db(self,
                              transaction_amount: int,
                              record_date: str,
                              category: str,
                              description: str,
                              telegram_id: int | None = None,
                              username: str | None = None) -> bool:
        """
        The function records user transactions in the database.

        :param username:
        :param telegram_id:
        :param transaction_amount: value of the deposited amount (can be both negative and positive)
        :param category:
        :param description:
        :param record_date:
        """
        if not telegram_id and not username:
            logger_database.error("telegram_id and username are None")
            return False
        params: dict = {
            'transaction_amount': transaction_amount,
            'record_date': record_date,
            'category': category,
            'description': description,
            'telegram_id': telegram_id,
            'username': username
        }
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('add_transaction_to_db'), params)
            return True

        except (DatabaseError, TypeError) as err:
            logger_database.error(
                f"[DB_QUERY] {str(err)}, "
                f"username (hash): {logging_hash(username) if username is not None else None}, "
                f"telegram_id (hash): {logging_hash(telegram_id) if telegram_id is not None else None}, "
                f"transaction_amount: {transaction_amount},"
                f"record_date: {record_date},"
                f"category: {category},"
                f"description: {description}"
            )
            return False

    def process_delete_transaction_record(self, group_id: int, transaction_id: int) -> bool:
        """
        Removes a record from the "monetary_transactions" table and then adjusts all later values in the "total" column
        so that the deleted record does not introduce artifacts for subsequent calculations
        """
        params: dict = {
            'group_id': group_id,
            'transaction_id': transaction_id
        }
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('delete_transaction_record'), params)
            return True

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"group ID: {group_id}, "
                                  f"transaction ID: {transaction_id}")
            return False

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    @timeit
    def registration_new_user(
            self,
            telegram_id: int,
            username: str,
            psw_salt: str,
            psw_hash: str,
            group_id: int | None = None
    ) -> bool | str:
        """
        This function is needed to be able to rollback a transaction when an error occurs in any request:
        in fact, there are 2-3 requests inside using the INSERT operator,
        which it is important for us to keep within one transaction.

        group_id = None - a sign if we are creating a new group and owner, and not an individual user

        IMPORTANT: when registering a new user, if the group is full, the transaction will be rejected
        (since the trigger to check the field value will be triggered),
        so an additional check of the number of participants in the group will be unnecessary

        :return:
        1. If owner registration is successful, it returns the group token (otherwise an empty string).
        2. If the user is successfully registered into an existing group, returns True (otherwise False)
        """
        group_token: str | None = get_token() if not group_id else None
        params: dict = {
            'telegram_id': telegram_id,
            'username': username,
            'psw_salt': psw_salt,
            'psw_hash': psw_hash,
            'group_id': group_id,
            'token': group_token
        }
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('new_user_in_group' if group_id else 'new_user_with_group'), params)
                    conn.commit()
            return group_token if group_token else True

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"telegram_id (hash): {logging_hash(telegram_id)}; "
                                  f"username (hash): {logging_hash(username)}; "
                                  f"group_id: {group_id}; "
                                  f"psw_salt - {bool(psw_salt)}; "
                                  f"psw_hash - {bool(psw_hash)}; "
                                  f"token = {group_token}")
            return '' if group_token else False

    def update_user_last_login_by_telegram_id(self, telegram_id: int) -> None | datetime:
        """
        Changes the user's last login time in the last_login column in the Users table.
        :return: None
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(read_sql_file('update_user_last_login_by_telegram_id'), {'telegram_id': telegram_id})
                    return res[0] if (res := cur.fetchone()) else None  # TODO - довести до datetime возвращаемое значение и покрыть тестами
        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"telegram_id: {logging_hash(telegram_id)}")
            return None

    def update_group_owner(self, new_owner_telegram_id: int, group_id: int) -> bool:
        """
        Changes the owner of a group to another user from that group
        """
        group_id_by_new_owner_telegram_id: int = self.get_group_id_by_telegram_id(new_owner_telegram_id)
        if group_id_by_new_owner_telegram_id != group_id:
            logger_database.warning(f"[DB_QUERY] group_id_by_new_owner != group_id, "
                                    f"telegram_id: {logging_hash(new_owner_telegram_id)}, "
                                    f"group_id_by_new_owner: {group_id_by_new_owner_telegram_id}, "
                                    f"group_id: {group_id}")
            return False

        current_group_owner: int = self.get_group_owner_telegram_id_by_group_id(group_id)
        if new_owner_telegram_id == current_group_owner:
            logger_database.warning(f"[DB_QUERY] new_owner_telegram_id == current_group_owner, "
                                    f"new_owner_telegram_id: {logging_hash(new_owner_telegram_id)}, "
                                    f"current_group_owner: {logging_hash(current_group_owner)}, "
                                    f"group_id: {group_id}")
            return False

        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        read_sql_file(
                            'update_group_owner'),
                        {'telegram_id': new_owner_telegram_id, 'group_id': group_id}
                    )
                    conn.commit()
            logger_database.info(f"Updated group owner: group_id = {logging_hash(group_id)},"
                                 f"telegram_id owner = {logging_hash(new_owner_telegram_id)}")
            return True

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"telegram_id: {logging_hash(new_owner_telegram_id)}, "
                                  f"group_id: {group_id}")
            return False

    def delete_user_from_group_by_telegram_id(self, telegram_id: int) -> bool:
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                                   DELETE FROM
                                     "budget_graph"."users_groups"
                                   WHERE
                                     "telegram_id" = %s::bigint;

                                   DELETE FROM
                                     "budget_graph"."users"
                                   WHERE
                                     "telegram_id" = %s::bigint
                                """, (telegram_id, telegram_id,))
                    conn.commit()
            logger_database.info(f"Telegram ID {logging_hash(telegram_id)} has been removed from the database")
            return True  # this is a flag of a successful operation, the user id may not exist in the database

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"telegram ID: {logging_hash(telegram_id)}")
            return False

    def delete_group_with_users(self, group_id: int) -> bool:  # TODO REFERENCES IN .sql
        """
        Deletes the group table along with all its members (including the owner)
        """
        try:
            with self.__conn as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                                    -- users
                                    WITH
                                    telegram_id_users AS (
                                        SELECT
                                         u."telegram_id"
                                       FROM
                                         "budget_graph"."users" u
                                       JOIN
                                         "budget_graph"."users_groups" u_g
                                       ON
                                         u."telegram_id" = u_g."telegram_id"
                                       WHERE
                                         u_g."group_id" = %s::smallint
                                    )
                                    
                                    DELETE FROM
                                        "budget_graph"."users"
                                    WHERE
                                        "telegram_id" = ANY(ARRAY(SELECT "telegram_id" FROM telegram_id_users));
                                    
                                    -- groups
                                    DELETE FROM
                                        "budget_graph"."groups"
                                    WHERE
                                        "id" = %s::smallint;
                                    
                                    -- users_groups
                                    DELETE FROM
                                        "budget_graph"."users_groups"
                                    WHERE
                                        "group_id" = %s::smallint;
                                    
                                    -- monetary_transactions
                                    DELETE FROM
                                        "budget_graph"."monetary_transactions"
                                    WHERE
                                        "group_id" = %s::smallint;
                    """, (*([group_id]*4),))

                    conn.commit()
            logger_database.info(f'[DB_QUERY] Group #{group_id} has been completely deleted')
            return True

        except (DatabaseError, TypeError) as err:
            logger_database.error(f"[DB_QUERY] {str(err)}, "
                                  f"group ID: {group_id}")
            return False
