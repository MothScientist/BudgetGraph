import os
import csv
from database_control import DatabaseQueries, connect_db, close_db_main
from log_settings import setup_logger
from source.time_checking import timeit

logger_csv = setup_logger("logs/SourceLog.log", "csv_logger")


def csv_dir_check():
    if not os.path.exists("csv_tables"):
        os.makedirs("csv_tables")


@timeit
def create_csv_file(group_id: int):
    connection = connect_db()
    db = DatabaseQueries(connection)
    data: list = db.select_data_for_household_table(group_id, 0)
    close_db_main(connection)
    csv_dir_check()  # to prevent possible "FileNotFoundError"
    with open(f"csv_tables/table_{group_id}.csv", 'w', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["ID", "TOTAL", "USERNAME", "TRANSFER", "CATEGORY","DATE_TIME", "DESCRIPTION"])
        for record in data:
            filewriter.writerow(record)

    file_size: int | float = get_file_size_kb(f"csv_tables/table_{group_id}.csv")

    logger_csv.info(f"Generated CSV file for group #{group_id} is completed. File size: {"{:.3f}".format(file_size)} kB")


@timeit
def delete_csv_file(group_id: int):
    try:
        os.remove(f"csv_tables/table_{group_id}.csv")
        logger_csv.info(f"Destroyed CSV file for group #{group_id}")
    except FileNotFoundError:
        logger_csv.error(f"The CSV file to delete was not found. Group #{group_id}")
    except PermissionError:
        logger_csv.error(f"The CSV file to delete busy with another process. Group #{group_id}")


def get_file_size_kb(file_path) -> int | float:
    """
    Returns the file size in kilobytes (float), if an error occurs, return value 0 (int)
    """
    try:
        file_size: int = os.path.getsize(file_path)
    except FileNotFoundError:
        logger_csv.error("An error occurred while trying to determine the file size.")
    else:
        return file_size / 1024
    return 0
