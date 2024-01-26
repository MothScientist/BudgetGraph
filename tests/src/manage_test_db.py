import sqlite3


def connect_test_db(db_path="src/test_db.sqlite3"):
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn

    except sqlite3.Error as err:
        print(str(err))


def close_test_db(conn):
    if conn:
        conn.close()


def create_test_db() -> None:
    try:
        conn = connect_test_db(db_path="test_db.sqlite3")
        cursor = conn.cursor()

        with open("create_test_db.sql", 'r') as file:
            cursor.executescript(file.read())

        conn.commit()
        close_test_db(conn)

    except sqlite3.Error as err:
        print(str(err))
