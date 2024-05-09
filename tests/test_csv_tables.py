# pylint: disable=missing-docstring

import os
import unittest
from pytest import raises

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

    # Case 1
    def test_csv_1(self):
        file_path: str = 'test_csv_tables/test_table_1.csv'
        create_csv_file(file_path, ('column_1', 'column_2', 'column_3'), (('1', '2', '3'), ('1', '2', '3')))
        self.assertEqual(os.path.exists(file_path), True)

        file_size: float = get_file_size_kb(file_path)
        file_size: str = "{:.3f}".format(file_size)
        self.assertEqual(file_size, '0.041')

        file_checksum: str = get_file_checksum(file_path)
        print(file_checksum)
        self.assertEqual(file_checksum, '8b443b2986f52ce0b30c6181749143024e565f0b38a8627f814af73735431d0f')


if __name__ == '__main__':
    unittest.main()
