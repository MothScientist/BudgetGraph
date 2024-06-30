import os
import unittest
from pytest import raises
from random import randint
from time import perf_counter

from budget_graph.create_csv import CsvFileWithTable


class TestCreateCSV(unittest.TestCase):
    # TODO - переделать после проверок на длину кортежей
    # def test_create_csv_1(self):  # empty parameters
    #     with raises(ValueError):
    #         csv_test_obj_1 = CsvFileWithTable('test_csv_tables/test_table_1.csv')
    #         validate_incoming_data('test_csv_tables/test_table_1.csv', (), ())
    #
    # def test_create_csv_2(self):
    #     with raises(ValueError):
    #         validate_incoming_data('test_csv_tables/test_table_1.csv', ('one', 'two', 'three'), ())
    #
    # def test_create_csv_3(self):
    #     with raises(ValueError):
    #         validate_incoming_data('test_csv_tables/test_table_1.csv', (),
    #                                (('one', 'one'), ('two', 'two'), ('three', 'three')))
    #
    # def test_create_csv_4(self):
    #     with raises(ValueError):
    #         validate_incoming_data('test_csv_tables/test_table_1.csv', (), ((), ('two', 'two'), ('three', 'three')))
    #
    # def test_create_csv_5(self):
    #     with raises(ValueError):
    #         validate_incoming_data('test_csv_tables/test_table_1.csv', (), (('one', 'one'), (), ('three', 'three')))
    #
    # def test_create_csv_6(self):
    #     with raises(ValueError):
    #         validate_incoming_data('test_csv_tables/test_table_1.csv', (), (('one', 'one'), ('two', 'two'), ()))
    #
    # def test_create_csv_7(self):  # empty path
    #     with raises(ValueError):
    #         validate_incoming_data()  # TODO - переделать после проверок на длину кортежей
    #
    # def test_create_csv_8(self):
    #     with raises(ValueError):
    #         validate_incoming_data('path', ('', '', ' '), ((1, 2, 5), (1, 2, 5), (1, 2, 5)))
    #
    # def test_create_csv_9(self):
    #     with raises(ValueError):
    #         validate_incoming_data('', ('123',), ((),))
    #
    # def test_create_csv_10(self):
    #     with raises(ValueError):
    #         validate_incoming_data('', ('123', '123'), ((),))
    #
    # def test_create_csv_11(self):
    #     with raises(ValueError):
    #         validate_incoming_data('test_csv_tables/test_table_1.csv', ('123', '123'), ((1, 2, 3, 4, 5, 6, 7),))

    def test_csv_1(self):
        file_path: str = 'test_csv_tables/test_table_1.csv'
        table_headers: tuple = ('column_1', 'column_2', 'column_3')
        table_data: tuple = (('1', '2', '3'), ('1', '2', '3'))
        create_csv_obj_1 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
        create_csv_obj_1.create_csv_file()
        self.assertEqual(os.path.exists(file_path), True)

        file_size: str = '{:.3f}'.format(create_csv_obj_1.get_file_size_kb())
        self.assertEqual(file_size, '0.041')

        file_checksum: str = create_csv_obj_1.get_file_checksum()
        self.assertEqual(file_checksum, '8b443b2986f52ce0b30c6181749143024e565f0b38a8627f814af73735431d0f')

# TODO - время генерации повесить на warnings
    # def test_csv_2(self):
    #     file_path: str = 'test_csv_tables/test_table_2.csv'
    #     headers: tuple = ('0','1','2','3','4','5','6','7','8','9')
    #     table_data: tuple = (
    #         tuple(
    #                 (
    #                     str(randint(10000000, 100000000)),
    #                     i,
    #                     randint(10000000, 100000000),
    #                     float(i),
    #                     str(randint(0,1))*(i % 10),
    #                     'data'*(i % 10),
    #                     str((i**2)//10),
    #                     str(i),
    #                     'None',
    #                     str(randint(100, 10000))
    #                 )
    #                 for i in range(10_000)))
    #     _start = perf_counter()
    #     create_csv_file(file_path, headers, table_data)
    #     _end = perf_counter()
    #
    #     self.assertEqual(os.path.exists(file_path), True)
    #
    #     self.assertEqual((_end - _start) < 0.1, True, f'File generation time: {_end - _start}')
    #
    #     file_size: str = "{:.3f}".format(get_file_size_kb(file_path))
    #     self.assertEqual(bool(file_size), True)
    #
    #     file_checksum: str = get_file_checksum(file_path)
    #     self.assertEqual(bool(file_checksum), True)
    #
    # def test_csv_3(self):
    #     file_path: str = 'test_csv_tables/test_table_3.csv'
    #     headers: tuple = ('0','1','2')
    #     table_data: tuple = (
    #         tuple(
    #                 (
    #                     str(i),
    #                     i,
    #                     'data'
    #                 )
    #                 for i in range(50_000)))
    #     _start = perf_counter()
    #     create_csv_file(file_path, headers, table_data)
    #     _end = perf_counter()
    #
    #     self.assertEqual(os.path.exists(file_path), True)
    #
    #     self.assertEqual((_end - _start) < 0.1, True, f'File generation time: {_end - _start}')
    #
    #     file_size: str = "{:.3f}".format(get_file_size_kb(file_path))
    #     self.assertEqual(file_size, '857.214')
    #
    #     file_checksum: str = get_file_checksum(file_path)
    #     self.assertEqual(file_checksum, '6dfa7cc1b0d4c7903f340b8c4adc91be6142a0037625693e3c4fa2928f9cdc55')
    #
    # def test_csv_4(self):
    #     file_path: str = 'test_csv_tables/test_table_4.csv'
    #     create_csv_file(file_path,
    #                     ('column_1', '0', '0'),
    #                     (
    #                         (0, 0, 0),
    #                         (0, 0, 'row_12'),
    #                         (0, 0, 0)
    #                     )
    #                     )
    #     self.assertEqual(os.path.exists(file_path), True)
    #
    #     file_size: float = get_file_size_kb(file_path)
    #     file_size: str = "{:.3f}".format(file_size)
    #     self.assertEqual(file_size != '0.000', True)
    #
    #     file_checksum: str = get_file_checksum(file_path)
    #     print(file_checksum)
    #     self.assertEqual(len(file_checksum) == 64, True)

# TODO - дописать тесты для заголовков по умолчанию


if __name__ == '__main__':
    unittest.main()
