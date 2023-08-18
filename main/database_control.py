from flask import g
import sqlite3


def connect_db():
    conn = sqlite3.connect("db.sqlite3")
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    conn = connect_db()
    cursor = conn.cursor()

    with open("create_db.sql", 'r') as file:
        cursor.executescript(file.read())

    conn.commit()
    conn.close()


# def insert_data():
#     conn = create_connection()
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO table_name (column1, column2, ...) VALUES (?, ?)", ('value1', 'value2'))
#     conn.commit()
#     conn.close()

def get_db():
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
        print("Database connection: OK")
    return g.link_db


def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()
        print("Database connection: CLOSED")


if __name__ == '__main__':
    create_db()
    # insert_data()
