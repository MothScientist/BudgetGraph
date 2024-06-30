from os import path as os_path
from csv import writer as csv_writer, QUOTE_MINIMAL
from hashlib import sha256


class CsvFileWithTable:
    """
    Class for working with *.csv files: creating, updating, obtaining the file hash, file size and validating user data
    """

    def __init__(self, file_path: str,
                 table_data: tuple[[tuple, ...], ...],
                 table_headers: tuple[str, ...] =
                 ('ID', 'USERNAME', 'TRANSFER', 'TOTAL', 'DATE', 'CATEGORY', 'DESCRIPTION')):
        self.file_path: str = file_path
        self.table_data: tuple[tuple[int, str, int, int, str, str, str], ...] = table_data
        self.table_headers: tuple[str, ...] = table_headers

    def create_csv_file(self):
        """
        The function is responsible for creating *.csv file
        """
        # data validation to fill the table
        self.validate_incoming_data()
        with open(self.file_path, 'w', newline='', encoding='utf-8') as csvfile:
            filewriter = csv_writer(csvfile, quoting=QUOTE_MINIMAL)
            filewriter.writerow(self.table_headers)
            for _data_row in self.table_data:
                filewriter.writerow(_data_row)

    def get_file_size_kb(self) -> float:
        """
        Returns the file size in kilobytes (float), if an error occurs, return value 0 (int)
        """
        file_size: int = os_path.getsize(self.file_path)
        return file_size / 1024

    def get_file_checksum(self) -> str:
        hash_sha256 = sha256()  # noqa
        with open(self.file_path, 'rb', encoding='utf-8') as csv_file:
            for chunk in iter(lambda: csv_file.read(1024), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    # TODO - а что если переделать это на дескриптор?
    def validate_incoming_data(self):
        """
        Checking the input data so that the application does not crash due to a *.csv generation error
        """
        # TODO - проверка на валидность директории -> мб есть функция готовая или тестовый ping сделать с отловом ошибки
        # table_data is never empty when calling a function
        if not self.table_headers:
            raise ValueError('table_headers values cannot be empty')
        # TODO - сделать проверку на отсутствие None и '' для всех вложенных кортежей
        if not self.table_data or not all(element is not None and element != '' for element in self.table_data):
            # not all(map(len, table_data)) -> no nested tuple is empty
            raise ValueError('table_data parameters cannot be empty')
        if not all(len(self.table_headers) == len(_row) for _row in self.table_data):
            # the length of each nested tuple is equal to the number of columns in the table
            raise ValueError('Data tuples have different lengths and/or their lengths do not match the headers')
