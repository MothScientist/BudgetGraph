import os
from database_control import create_db

if __name__ == '__main__':
    if not os.path.exists("csv_tables"):
        os.makedirs("csv_tables")

    create_db()
