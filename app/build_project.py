from app.database_control import create_db
from app.csv_file_generation_and_deletion import csv_dir_check
from os import makedirs

if __name__ == '__main__':
    create_db()
    csv_dir_check()
    makedirs("logs", exist_ok=True)
