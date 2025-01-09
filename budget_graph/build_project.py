from os import makedirs, path
from sys import path as sys_path
sys_path.append('../')
from budget_graph.db_manager import connect_db, close_db
from budget_graph.global_config import GlobalConfig


def drop_tables_in_db() -> None:
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            with open(path.join(path.dirname(__file__), 'sql/db_cleanup.sql'), 'r', encoding='utf-8') as sql_file:
                cur.execute(sql_file.read())
            conn.commit()
    # pylint: disable=broad-exception-caught
    except Exception as err:
        print(f'Critical error when deleting tables in the database: {err}')
    finally:
        close_db(conn)


def create_directories() -> None:
    try:
        makedirs('csv_tables', exist_ok=True)
        makedirs('logs', exist_ok=True)
    # pylint: disable=broad-exception-caught
    except Exception as err:
        print(f'Error creating additional directories: {err}')


def create_tables_in_db() -> None:
    """
    Creating a Database Infrastructure
    """
    conn = connect_db()

    # sql scripts to run before running the application
    sql_filenames: tuple = (
        'create_db',
        'indexes',
        'func_transaction_number',
        'func_auto_count_users_of_group',
        'update_group_uuid_after_transaction'
    )

    try:
        with conn.cursor() as cur:
            for filename in sql_filenames:
                with open(path.join(path.dirname(__file__), f'sql/{filename}.sql'), 'r', encoding='utf-8') as sql_file:
                    cur.execute(sql_file.read())
            conn.commit()
    # pylint: disable=broad-exception-caught
    except Exception as err:
        print(f'Critical error when creating tables in the database: {err}')
    finally:
        close_db(conn)


def load_global_config() -> None:
    GlobalConfig.set_config()


if __name__ == '__main__':
    load_global_config()
    create_directories()
    drop_tables_in_db()
    create_tables_in_db()
