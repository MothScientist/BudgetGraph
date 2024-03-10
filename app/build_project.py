import sys
sys.path.append('../')
from app.db_manager import connect_db, close_db  # noqa


def create_db() -> None:
    """
    Creates tables, using create_db.sql file describing their structures.
    """
    conn = connect_db()
    try:
        with conn.cursor() as cur:
            with open("create_db.sql", 'r') as file:
                cur.execute(file.read())

            conn.commit()

    except Exception as err:
        print(f"Critical error when creating tables in the database: {err}")

    finally:
        close_db(conn)


if __name__ == '__main__':
    create_db()
