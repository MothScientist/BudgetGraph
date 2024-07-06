from os import path as os_path
from csv import writer as csv_writer, QUOTE_MINIMAL
from hashlib import sha256

from budget_graph.dictionary import receive_translation


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
        # translate if it matches the standard set of headers
        if table_data == ('ID', 'USERNAME', 'TRANSFER', 'TOTAL', 'DATE', 'CATEGORY', 'DESCRIPTION') and lang != 'en':
            self.table_data = (receive_translation(lang, 'ID'),
                               receive_translation(lang, 'USERNAME'),
                               receive_translation(lang, 'TRANSFER'),
                               receive_translation(lang, 'TOTAL'),
                               receive_translation(lang, 'DATE'),
                               receive_translation(lang, 'CATEGORY'),
                               receive_translation(lang, 'DESCRIPTION'))

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
        try:
            file_size: int = os_path.getsize(self.file_path)
        except FileNotFoundError:
            return 0
        return file_size / 1024

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
