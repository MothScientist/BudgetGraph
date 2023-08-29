from flask import g
import sqlite3
from hmac import compare_digest


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    # def check_user_by_username(self, username):
    #     sql = """SELECT * FROM Users WHERE username = ?"""
    #     try:
    #         self.__cur.execute(sql, (username,))
    #         res = self.__cur.fetchall()
    #         if res:
    #             return True
    #     except sqlite3.Error as e:
    #         print(str(e))
    #     return False

    def auth_by_username(self, username: str, psw_hash: str, token: str):
        # The first stage of verification: using username, we verify the password and get the user's group id
        sql = """SELECT password_hash, group_id FROM Users WHERE username = ?"""
        try:
            self.__cur.execute(sql, (username,))
            res = self.__cur.fetchall()
            if res:  # if data for such username exists
                psw, group = res[0]  # get password_hash и group_id from database
                if compare_digest(psw, psw_hash):  # if the password matches / safe string comparison
                    psw = "EMPTY"  # overwriting a variable for safety

                    # The second stage of verification: we verify the token by the group id
                    sql = """SELECT token FROM Groups WHERE id = ?"""
                    try:
                        self.__cur.execute(sql, (group,))
                        res = self.__cur.fetchone()
                        if res:
                            if compare_digest(res[0], token):  # safe string comparison
                                return True  # if the token matches the group token
                    except sqlite3.Error as e:
                        print(str(e))

        except sqlite3.Error as e:
            print(str(e))


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
