# pylint: disable=missing-docstring
# pylint: disable=trailing-whitespace

import os
import unittest
from pytest import raises
from random import randint
from time import perf_counter

from budget_graph.create_csv import create_csv_file, get_file_size_kb, get_file_checksum


class TestCreateCSV(unittest.TestCase):
    def test_create_csv_1(self):  # empty parameters
        with raises(ValueError):
            create_csv_file('any', (), ())

    def test_create_csv_2(self):
        with raises(ValueError):
            create_csv_file('any', ('one', 'two', 'three'), ())

    def test_create_csv_3(self):
        with raises(ValueError):
            create_csv_file('any', (), (('one', 'one'), ('two', 'two'), ('three', 'three')))

    def test_create_csv_4(self):
        with raises(ValueError):
            create_csv_file('any', (), ((), ('two', 'two'), ('three', 'three')))

    def test_create_csv_5(self):
        with raises(ValueError):
            create_csv_file('any', (), (('one', 'one'), (), ('three', 'three')))

    def test_create_csv_6(self):
        with raises(ValueError):
            create_csv_file('any', (), (('one', 'one'), ('two', 'two'), ()))

    def test_csv_1(self):
        file_path: str = 'test_csv_tables/test_table_1.csv'
        create_csv_file(file_path, ('column_1', 'column_2', 'column_3'), (('1', '2', '3'), ('1', '2', '3')))
        self.assertEqual(os.path.exists(file_path), True)

        file_size: str = "{:.3f}".format(get_file_size_kb(file_path))
        self.assertEqual(file_size, '0.041')

        file_checksum: str = get_file_checksum(file_path)
        self.assertEqual(file_checksum, '8b443b2986f52ce0b30c6181749143024e565f0b38a8627f814af73735431d0f')

    def test_csv_2(self):
        file_path: str = 'test_csv_tables/test_table_2.csv'
        headers: tuple = (0,1,2,3,4,5,6,7,8,9)
        table_data: tuple = (
            tuple(
                    (
                        str(randint(10000000, 100000000)),
                        i,
                        randint(10000000, 100000000),
                        float(i),
                        str(randint(0,1))*(i % 10),
                        'data'*(i % 10),
                        str((i**2)//10),
                        str(i),
                        'None',
                        str(randint(100, 10000))
                    )
                    for i in range(10_000)))
        _start = perf_counter()
        create_csv_file(file_path, headers, table_data)
        _end = perf_counter()

        self.assertEqual(os.path.exists(file_path), True)

        self.assertEqual((_end - _start) < 0.1, True, f'File generation time: {_end - _start}')

        file_size: str = "{:.3f}".format(get_file_size_kb(file_path))
        self.assertEqual(bool(file_size), True)

        file_checksum: str = get_file_checksum(file_path)
        self.assertEqual(bool(file_checksum), True)

    def test_csv_3(self):
        file_path: str = 'test_csv_tables/test_table_3.csv'
        headers: tuple = (0,1,2)
        table_data: tuple = (
            tuple(
                    (
                        str(i),
                        i,
                        'data'
                    )
                    for i in range(50_000)))
        _start = perf_counter()
        create_csv_file(file_path, headers, table_data)
        _end = perf_counter()

        self.assertEqual(os.path.exists(file_path), True)

        self.assertEqual((_end - _start) < 0.1, True, f'File generation time: {_end - _start}')

        file_size: str = "{:.3f}".format(get_file_size_kb(file_path))
        self.assertEqual(file_size, '857.214')

        file_checksum: str = get_file_checksum(file_path)
        self.assertEqual(file_checksum, '6dfa7cc1b0d4c7903f340b8c4adc91be6142a0037625693e3c4fa2928f9cdc55')


if __name__ == '__main__':
    unittest.main()
