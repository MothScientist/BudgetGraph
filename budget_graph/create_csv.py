import os
import csv
import hashlib


def create_csv_file(file_path: str, table_headers: tuple, table_data: tuple[tuple, ...]) -> None:
    if not table_headers or not table_data or not all(map(len, table_data)):
        raise ValueError('table_headers and table_data parameters cannot be empty')
    # if ...:  # TODO - сделать проверку, что длина table_headers равна длине каждого кортежа внутри table_data
    #     raise ValueError('')
    with open(file_path, 'w', newline='',  encoding="utf-8") as csvfile:
        filewriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(table_headers)
        for _data in table_data:
            filewriter.writerow(_data)


def get_file_size_kb(file_path: str) -> float:
    """
    Returns the file size in kilobytes (float), if an error occurs, return value 0 (int)
    """
    file_size: int = os.path.getsize(file_path)
    return file_size / 1024


def get_file_checksum(file_path: str) -> str:
    hash_sha256 = hashlib.sha256()  # TODO
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


if __name__ == '__main__':
    pass