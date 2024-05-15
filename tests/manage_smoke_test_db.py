# pylint: disable=missing-docstring
# pylint: disable=trailing-whitespace

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
db_host = os.getenv("POSTGRES_HOST_TEST")
db_port = os.getenv("POSTGRES_PORT_TEST")
db_name = os.getenv("POSTGRES_NAME_TEST")
db_user = os.getenv("POSTGRES_USERNAME_TEST")
db_psw = os.getenv("POSTGRES_PASSWORD_TEST")

DSN = f"dbname={db_name} user={db_user} password={db_psw} host={db_host} port={db_port}"


def connect_test_db():
    try:
        conn = psycopg2.connect(DSN)
        return conn

    except Exception as err:
        print(err)


def close_test_db(conn):
    if conn:
        conn.close()


def create_smoke_test_db() -> None:
    """
    Creates tables, using create_db.sql file describing their structures.
    """
    conn = connect_test_db()
    try:
        with conn.cursor() as cur:
            with open("create_smoke_test_db.sql", 'r') as file:
                cur.execute(file.read())

            conn.commit()

    except Exception as err:
        print(err)

    finally:
        close_test_db(conn)


if __name__ == "__main__":
    create_smoke_test_db()
