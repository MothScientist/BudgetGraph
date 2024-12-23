from os import path as os_path
from csv import writer as csv_writer, QUOTE_MINIMAL
from hashlib import sha256

from budget_graph.logger import setup_logger
from budget_graph.dictionary import receive_translation

logger_csv_builder = setup_logger("logs/CsvLog.log", "csv_builder_logger")


class CsvFileWithTable:
    """
    Class for working with *.csv files: creating, updating, obtaining the file hash, file size and validating user data
    """
    def __init__(self, file_path: str,
                 table_data: tuple[[tuple, ...], ...],
                 table_headers: tuple[str, ...] =
                 ('ID', 'USERNAME', 'TRANSFER', 'TOTAL', 'DATE', 'CATEGORY', 'DESCRIPTION'),
                 lang: str = 'en'):
        self.file_path: str = file_path
        self.table_data: tuple[tuple, ...] = table_data
        self.table_headers: tuple[str, ...] = table_headers
        self.language: str = lang

    def create_csv_file(self):
        """
        The function is responsible for creating *.csv file
        """
        # translate if it matches the standard set of headers
        if (self.table_headers == ('ID', 'USERNAME', 'TRANSFER', 'TOTAL', 'DATE', 'CATEGORY', 'DESCRIPTION')
                and self.language != 'en'):
            self.table_headers = (receive_translation(self.language, 'ID'),
                                  receive_translation(self.language, 'USERNAME'),
                                  receive_translation(self.language, 'TRANSFER'),
                                  receive_translation(self.language, 'TOTAL'),
                                  receive_translation(self.language, 'DATE'),
                                  receive_translation(self.language, 'CATEGORY'),
                                  receive_translation(self.language, 'DESCRIPTION'))

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
        try:
            file_size: int = os_path.getsize(self.file_path)
            kb_size: float = file_size / 1024
        except (FileNotFoundError, ZeroDivisionError) as err:
            logger_csv_builder.warning(f'Error calculating CSV file size: {err}')
            return 0
        logger_csv_builder.info(f'CSV file successfully created with size: {kb_size} kB')
        return kb_size

    def get_file_checksum(self) -> str:
        hash_sha256 = sha256()
        try:
            with open(self.file_path, 'rb') as csv_file:
                for chunk in iter(lambda: csv_file.read(1024), b''):
                    hash_sha256.update(chunk)
        except FileNotFoundError:
            return ''
        return hash_sha256.hexdigest()

    def validate_incoming_data(self):
        """
        Checking the input data so that the application does not crash due to a *.csv generation error
        """
        # we get the path to the directory in which we are going to save the file
        path_lst: list = self.file_path.split('/')[:-1]
        path_to_directory: str = '/'.join(path_lst)
        if not os_path.exists(path_to_directory):
            raise FileNotFoundError('The path specified to save the CSV file is incorrect')
        # table_data is never empty when calling a function
        if not self.table_headers or not all(bool(header) for header in self.table_headers):
            raise ValueError('Table headers values cannot be empty')
        # the length of each nested tuple is equal to the number of columns in the table
        if not all(len(self.table_headers) == len(_row) for _row in self.table_data):
            raise ValueError('Data tuples have different lengths and/or their lengths do not match the headers')


def check_csv_is_actual(group_id: int, group_uuid: str) -> bool:
    """
    Checks for the presence of an up-to-date file, if there is one, returns True, otherwise False
    If this group already has such a file, but its uuid is not up-to-date, then deletes it
    """
    if os_path.isfile(f'csv_tables/{group_id}_{group_uuid}.csv'):
        return True
