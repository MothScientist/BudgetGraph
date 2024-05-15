import os
import csv
import hashlib


# TODO - проверить время генерации при заполнении в 10_000 строк
def create_csv_file(file_path: str, table_headers: tuple, table_data: tuple[tuple, ...]) -> None:
    if not table_headers or not table_data or not all(map(len, table_data)):
        # not all(map(len, table_data)) -> no nested tuple is empty
        raise ValueError('table_headers and table_data parameters cannot be empty')  # TODO lang
    elif not all(len(table_headers) == len(_row) for _row in table_data):
        # the length of each nested tuple is equal to the number of columns in the table
        raise ValueError('разная длина кортежей данных и/или их длина не сходится с размерами таблицы')  # TODO lang

    with open(file_path, 'w', newline='',  encoding="utf-8") as csvfile:
        filewriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(table_headers)
        for _data_row in table_data:
            filewriter.writerow(_data_row)


def get_file_size_kb(file_path: str) -> float:
    """
    Returns the file size in kilobytes (float), if an error occurs, return value 0 (int)
    """
    file_size: int = os.path.getsize(file_path)
    return file_size / 1024


def get_file_checksum(file_path: str) -> str:
    hash_sha256 = hashlib.sha256()  # noqa
    with open(file_path, 'rb') as csv_file:
        for chunk in iter(lambda: csv_file.read(1024), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()
