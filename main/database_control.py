from flask import g
import sqlite3
from hmac import compare_digest
from datetime import datetime


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def token_verification(self, token: str):
        try:
            self.__cur.execute("""SELECT id FROM Groups WHERE token = ?""", (token,))
            res = self.__cur.fetchone()
            if res:
                return res[0]
        except sqlite3.Error as e:
            print(str(e))

    def user_exist(self, tg_link: str):
        try:
            self.__cur.execute("""SELECT id FROM Users WHERE telegram_link = ?""", (tg_link,))
            res = self.__cur.fetchone()
            if res:  # res[0] = None if the user with this link does not exist
                return True
        except sqlite3.Error as e:
            print(str(e))

        return False

    def auth_by_username(self, username: str, psw_hash: str, token: str):
        # The first stage of verification: using username, we verify the password and get the user's group id
        try:
            self.__cur.execute("""SELECT password_hash, group_id FROM Users WHERE username = ?""", (username,))
            res = self.__cur.fetchall()
            if res:  # if data for such username exists
                psw, group = res[0]  # get password_hash и group_id from database
                if compare_digest(psw, psw_hash):  # if the password matches / safe string comparison
                    psw = "EMPTY"  # overwriting a variable for safety

                    # The second stage of verification: we verify the token by the group id
                    try:
                        self.__cur.execute("""SELECT token FROM Groups WHERE id = ?""", (group,))
                        res = self.__cur.fetchone()
                        if res:
                            if compare_digest(res[0], token):  # safe string comparison
                                return True  # if the token matches the group token
                    except sqlite3.Error as e:
                        print(str(e))

        except sqlite3.Error as e:
            print(str(e))

    def add_user_to_group(self, username: str, psw_hash: str, group_id: int, tg_link: str):
        try:
            self.__cur.execute("INSERT INTO Users VALUES(NULL, ?, ?, ?, ?, ?)",
                               (username, psw_hash, group_id, tg_link, datetime.now().strftime("%d-%m-%Y %H:%M"),))
            self.__db.commit()

        except sqlite3.Error as e:
            print(str(e))
            return False

        return True


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
