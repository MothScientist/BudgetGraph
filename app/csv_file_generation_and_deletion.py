import os
import csv


def csv_dir_check():
    if not os.path.exists("csv_tables"):
        os.makedirs("csv_tables")


def create_csv_file(file_path: str, table_headers: tuple | list, table_data: tuple | list) -> None:
    csv_dir_check()  # to prevent possible "FileNotFoundError"
    with open(file_path, 'w', newline='',  encoding="utf-8") as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(table_headers)
        for _data in table_data:
            filewriter.writerow(_data)


def get_file_size_kb(file_path: str) -> int | float:
    """
    Returns the file size in kilobytes (float), if an error occurs, return value 0 (int)
    """
    file_size: int = os.path.getsize(file_path)
    return file_size / 1024


def get_file_hash(file_path: str) -> str:  # TODO
    return "soon"
