from os import getenv, makedirs
from psycopg2 import connect
from dotenv import load_dotenv
from sys import path as sys_path
sys_path.append('../')
from budget_graph.build_project import create_tables_in_db, drop_tables_in_db

load_dotenv()  # Load environment variables from .env file
db_host = getenv("POSTGRES_HOST")
db_port = getenv("POSTGRES_PORT")
db_name = getenv("POSTGRES_NAME")
db_user = getenv("POSTGRES_USERNAME")
db_psw = getenv("POSTGRES_PASSWORD")

DSN = f"dbname={db_name} user={db_user} password={db_psw} host={db_host} port={db_port}"


def prepare_db_tables_for_tests() -> None:
    drop_tables_in_db()
    create_tables_in_db()


def build() -> None:
    makedirs('logs', exist_ok=True)


def connect_test_db():
    try:
        conn = connect(DSN)
        return conn
    except Exception as err:
        print(f'Error connecting to database: {err}')


def close_test_db(conn) -> None:
    if conn:
        conn.close()


if __name__ == '__main__':
    prepare_db_tables_for_tests()
