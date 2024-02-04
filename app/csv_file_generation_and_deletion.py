import os
import csv
import hashlib


def create_csv_file(file_path: str, table_headers: tuple | list, table_data: tuple | list) -> None:
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


def get_file_checksum(file_path: str) -> str:
    hash_sha256 = hashlib.sha256()  # TODO
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(1024), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()
