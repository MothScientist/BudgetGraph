from os import makedirs, path
from sys import path as sys_path
sys_path.append('../')
from budget_graph.db_manager import connect_db, close_db  # noqa


def drop_tables_in_db() -> None:
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            cur.execute("""DROP TABLE IF EXISTS "budget_graph"."groups";
                           DROP TABLE IF EXISTS "budget_graph"."users";
                           DROP TABLE IF EXISTS "budget_graph"."monetary_transactions";
                           DROP TABLE IF EXISTS "budget_graph"."user_languages_telegram";
                           DROP TABLE IF EXISTS "budget_graph"."premium_users";
                           DROP TABLE IF EXISTS "budget_graph"."premium_groups"
                        """)
            conn.commit()
    except Exception as err:
        print(f'Critical error when deleting tables in the database: {err}')
    finally:
        close_db(conn)


def create_directories() -> None:
    try:
        makedirs('csv_tables', exist_ok=True)
        makedirs('logs', exist_ok=True)
    except Exception as err:
        print(f'Error creating additional directories: {err}')


def create_tables_in_db() -> None:
    """
    Creating a Database Infrastructure
    """
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            create_db_path: str = path.join(path.dirname(__file__), f'sql/create_db.sql')
            indexes_path: str = path.join(path.dirname(__file__), f'sql/indexes.sql')
            func_transaction_number_path: str = path.join(path.dirname(__file__),
                                                             f'sql/func_transaction_number.sql')
            func_auto_count_users_of_group_path: str = path.join(path.dirname(__file__),
                                                                    f'sql/func_auto_count_users_of_group.sql')
            with open(create_db_path, 'r') as file_1:
                cur.execute(file_1.read())
            with open(indexes_path, 'r') as file_2:
                cur.execute(file_2.read())
            with open(func_transaction_number_path, 'r') as file_3:
                cur.execute(file_3.read())
            with open(func_auto_count_users_of_group_path, 'r') as file_4:
                cur.execute(file_4.read())
            conn.commit()
    except Exception as err:
        print(f'Critical error when creating tables in the database: {err}')
    finally:
        close_db(conn)


if __name__ == '__main__':
    create_directories()
    create_tables_in_db()
