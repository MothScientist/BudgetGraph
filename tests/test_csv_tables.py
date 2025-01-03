from os import makedirs, path
from shutil import rmtree
import unittest
from random import randint, choice, seed
from time import perf_counter
from uuid import uuid4
from string import ascii_letters, digits

from budget_graph.create_csv import CsvFileWithTable


class TestCreateCSV(unittest.TestCase):
    # Let's set pre-computed sequences to speed up test execution
    tuple_of_500: tuple = tuple(range(500))
    tuple_of_1k: tuple = tuple(range(1000))
    tuple_of_10k: tuple = tuple(range(10_000))
    tuple_of_100k: tuple = tuple(range(100_000))

    @classmethod
    def setUpClass(cls):
        makedirs('test_csv_tables', exist_ok=True)
        rmtree('../budget_graph/__pycache__', ignore_errors=True)
        rmtree('.pytest_cache', ignore_errors=True)
        rmtree('__pycache__', ignore_errors=True)

    @classmethod
    def tearDownClass(cls):
        rmtree('test_csv_tables', ignore_errors=True)
        rmtree('../budget_graph/__pycache__', ignore_errors=True)
        rmtree('.pytest_cache', ignore_errors=True)
        rmtree('__pycache__', ignore_errors=True)

    def test_csv_001(self):
        file_path: str = 'test_csv_tables/test_table_1.csv'
        table_headers: tuple = ('column_1', 'column_2', 'column_3')
        table_data: tuple = (('1', '2', '3'), ('1', '2', '3'))
        create_csv_obj_1 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
        create_csv_obj_1.create_csv_file()
        self.assertTrue(path.exists(file_path))

        file_size: str = '{:.3f}'.format(create_csv_obj_1.get_file_size_kb())
        self.assertEqual(file_size, '0.041')

        file_checksum: str = create_csv_obj_1.get_file_checksum()
        self.assertEqual(file_checksum, '8b443b2986f52ce0b30c6181749143024e565f0b38a8627f814af73735431d0f')

    def test_csv_002(self):
        file_path: str = 'test_csv_tables/test_table_2.csv'
        table_headers: tuple = ('column_1',)
        table_data: tuple = (('1',),)
        create_csv_obj_2 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
        create_csv_obj_2.create_csv_file()
        self.assertTrue(path.exists(file_path))

        file_size: str = '{:.3f}'.format(create_csv_obj_2.get_file_size_kb())
        self.assertEqual(file_size, '0.013')

        file_checksum: str = create_csv_obj_2.get_file_checksum()
        self.assertEqual(file_checksum, '2322be3d68b9c3071c14ccdd4e8585359b06e1a784c41f904f21c0df395c58d2')

    def test_csv_003(self):
        file_path: str = 'test_csv_tables/100_000_columns.csv'
        table_headers: tuple = tuple(f'column_{i}' for i in TestCreateCSV.tuple_of_1k)
        table_data: tuple = (TestCreateCSV.tuple_of_1k,)
        create_csv_obj_3 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
        create_csv_obj_3.create_csv_file()
        self.assertTrue(path.exists(file_path))

        file_size: str = '{:.3f}'.format(create_csv_obj_3.get_file_size_kb())
        self.assertEqual(file_size, '14.436')

        file_checksum: str = create_csv_obj_3.get_file_checksum()
        self.assertEqual(file_checksum, '82f2c6d186f00f625a478a33d7efa131aab45fcae4cd106533026f17f85402f8')

    def test_csv_004(self):
        file_path: str = 'test_csv_tables/100_000_rows.csv'
        table_headers: tuple = tuple(f'column_{i}' for i in range(10))
        table_data: tuple = tuple((tuple(range(10))) for _ in TestCreateCSV.tuple_of_100k)
        create_csv_obj_4 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
        create_csv_obj_4.create_csv_file()
        self.assertTrue(path.exists(file_path))

        file_size: str = '{:.3f}'.format(create_csv_obj_4.get_file_size_kb())
        self.assertEqual(file_size, '2050.870')

        file_checksum: str = create_csv_obj_4.get_file_checksum()
        self.assertEqual(file_checksum, '29aa20b7dce537ebcef1bcb54ac5d8d8ee29b3d074402f6994b5294631ff95e7')

    def test_csv_005(self):
        """ The header tuple is longer than the length of the nested tuples """
        file_path: str = 'test_csv_tables/table_5.csv'
        table_headers: tuple = tuple(f'column_{i}' for i in range(100))
        table_data: tuple = tuple((tuple(range(10))) for _ in range(10))
        create_csv_obj_5 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
        with self.assertRaises(ValueError):
            create_csv_obj_5.create_csv_file()

    def test_csv_006(self):
        """ The header tuple is longer than the length of the nested tuples """
        file_path: str = 'test_csv_tables/table_6.csv'
        table_headers: tuple = ('123', '123', '123')
        table_data: tuple = (('qwerty', 'qwerty'), ('qwerty', 'qwerty'), ('qwerty', 'qwerty'),
                             ('qwerty', 'qwerty'), ('qwerty', 'qwerty'), ('qwerty', 'qwerty'))
        create_csv_obj_6 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
        with self.assertRaises(ValueError):
            create_csv_obj_6.create_csv_file()

    def test_csv_007(self):
        """ One of the headers is empty """
        file_path: str = 'test_csv_tables/table_7.csv'
        table_headers: tuple = ('column_1', '', 'column_3')
        table_data: tuple = (('1', '2', '3'), ('1', '2', '3'))
        create_csv_obj_7 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
        with self.assertRaises(ValueError):
            create_csv_obj_7.create_csv_file()

    def test_csv_008(self):
        """ One of the nested tuples does not match the length of the headers tuple """
        file_path: str = 'test_csv_tables/table_8.csv'
        table_headers: tuple = ('column_1', '', 'column_3')
        table_data: tuple = (('1', '2', '3'), ('1', '2', '3'), ('1', '2'))
        create_csv_obj_8 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
        with self.assertRaises(ValueError):
            create_csv_obj_8.create_csv_file()

    def test_csv_009(self):
        """ test_csv_007 + test_csv_008 """
        file_path: str = 'test_csv_tables/table_9.csv'
        table_headers: tuple = ('column_1', '', 'column_3')
        table_data: tuple = (('1', '2', '3'), ('1', '2', '3'))
        create_csv_obj_9 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
        with self.assertRaises(ValueError):
            create_csv_obj_9.create_csv_file()

    def test_csv_010(self):
        """ Checking that the file does not exist after invalid data validation """
        file_path: str = 'test_csv_tables/table_10.csv'
        table_headers: tuple = ('123', '123', '')
        table_data: tuple = (('1', '2', '3'),)
        create_csv_obj_10 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
        with self.assertRaises(ValueError):
            create_csv_obj_10.create_csv_file()
        file_size: str = '{:.3f}'.format(create_csv_obj_10.get_file_size_kb())
        self.assertEqual(file_size, '0.000')
        file_checksum: str = create_csv_obj_10.get_file_checksum()
        self.assertEqual(file_checksum, '')

    def test_csv_011(self):
        """ In this test we will create an object with the correct data so that we can reuse this object later """
        file_path: str = 'test_csv_tables/reuse.csv'
        table_headers: tuple = tuple(f'column_{i}' for i in range(100))
        table_data: tuple = tuple((tuple(range(100))) for _ in range(250))
        create_csv_obj_11 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
        create_csv_obj_11.create_csv_file()
        self.assertTrue(path.exists(file_path))

        file_size: str = '{:.3f}'.format(create_csv_obj_11.get_file_size_kb())
        self.assertEqual(file_size, '72.013')

        file_checksum: str = create_csv_obj_11.get_file_checksum()
        self.assertEqual(file_checksum, 'bda87f10dd11db5fff889c160f69a69f77b7b069871d5ebee4c8e22701f5c4ff')

    def test_csv_012(self):
        """
        We use the object from test_csv_11 and check that the data was successfully changed
        -> the hash amount has changed
        """
        file_path: str = 'test_csv_tables/reuse.csv'  # writing to the same file
        table_headers: tuple = tuple(f'column_{i}' for i in TestCreateCSV.tuple_of_500)
        table_data: tuple = tuple(TestCreateCSV.tuple_of_500 for _ in TestCreateCSV.tuple_of_1k)
        create_csv_obj_11 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
        create_csv_obj_11.create_csv_file()
        self.assertTrue(path.exists(file_path))

        file_size: str = '{:.3f}'.format(create_csv_obj_11.get_file_size_kb())
        self.assertEqual(file_size, '1851.944')

        file_checksum: str = create_csv_obj_11.get_file_checksum()
        self.assertEqual(file_checksum, 'ca99803e08673c0f59b84e3aa18a0aafac7b9d01ee23ef9e6ee9403795add366')

    def test_csv_013(self):
        """ Checking the generation time of a table for 10_000 rows filled with random data """
        file_path: str = 'test_csv_tables/table_13.csv'
        table_headers: tuple = tuple(f'column_{i}' for i in range(10))
        table_data: tuple = tuple((tuple(randint(10, 1_000_000)
                                   for _ in range(10))) for _ in TestCreateCSV.tuple_of_10k)
        create_csv_obj_13 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)

        start_generation_csv_file: float = perf_counter()
        create_csv_obj_13.create_csv_file()
        finish_generation_csv_file: float = perf_counter()
        time: float = finish_generation_csv_file - start_generation_csv_file
        self.assertTrue(time < 0.1, f'Time: {time}')

        # due to random data, checking the file size and hash does not make sense
        self.assertTrue(path.exists(file_path))

    def test_csv_014(self):
        """ Padding for 10_000 rows with default table_headers value """
        file_path: str = 'test_csv_tables/table_14.csv'  # writing to the same file
        table_data: tuple = tuple((tuple(range(7))) for _ in TestCreateCSV.tuple_of_10k)
        create_csv_obj_14 = CsvFileWithTable(file_path, table_data)

        start_generation_csv_file: float = perf_counter()
        create_csv_obj_14.create_csv_file()
        finish_generation_csv_file: float = perf_counter()
        time: float = finish_generation_csv_file - start_generation_csv_file
        self.assertTrue(time < 0.05, f'Time (create_csv_file): {time}')

        self.assertTrue(path.exists(file_path))

        start_generation_csv_file: float = perf_counter()
        file_size: str = '{:.3f}'.format(create_csv_obj_14.get_file_size_kb())
        finish_generation_csv_file: float = perf_counter()
        time = finish_generation_csv_file - start_generation_csv_file
        self.assertTrue(time < 0.002, f'Time (file_size): {time}')

        self.assertEqual(file_size, '146.537')

        start_generation_csv_file: float = perf_counter()
        file_checksum: str = create_csv_obj_14.get_file_checksum()
        finish_generation_csv_file: float = perf_counter()
        time = finish_generation_csv_file - start_generation_csv_file
        self.assertTrue(time < 0.002, f'Time (file_checksum): {time}')

        self.assertEqual(file_checksum, '3f3253daefa6606cade9358df918194c26307d475bc02008c9d9145adeff35d0')

    def test_csv_015(self):
        """ Padding for 100_000 rows with default table_headers value """
        file_path: str = 'test_csv_tables/table_15.csv'  # writing to the same file
        table_data: tuple = tuple((tuple(range(7))) for _ in TestCreateCSV.tuple_of_100k)
        create_csv_obj_15 = CsvFileWithTable(file_path, table_data)

        start_generation_csv_file: float = perf_counter()
        create_csv_obj_15.create_csv_file()
        finish_generation_csv_file: float = perf_counter()
        time: float = finish_generation_csv_file - start_generation_csv_file
        self.assertTrue(time < 0.5, f'Time (create_csv_file): {time}')

        self.assertTrue(path.exists(file_path))

        start_generation_csv_file: float = perf_counter()
        file_size: str = '{:.3f}'.format(create_csv_obj_15.get_file_size_kb())
        finish_generation_csv_file: float = perf_counter()
        time = finish_generation_csv_file - start_generation_csv_file
        self.assertTrue(time < 0.01, f'Time (file_size): {time}')

        self.assertEqual(file_size, '1464.896')

        start_generation_csv_file: float = perf_counter()
        file_checksum: str = create_csv_obj_15.get_file_checksum()
        finish_generation_csv_file: float = perf_counter()
        time = finish_generation_csv_file - start_generation_csv_file
        self.assertTrue(time < 0.01, f'Time (file_checksum): {time}')

        self.assertEqual(file_checksum, 'a2004facf77362035189c916cf432d0f88ad55df89a2817835c1b409f74254e6')

    def test_csv_016(self):
        file_path: str = 'test_csv_tables/table_16.csv'
        table_headers: tuple = ('123', '123', '123')
        table_data: tuple = (('1', '2', '3'), ())
        create_csv_obj_16 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
        with self.assertRaises(ValueError):
            create_csv_obj_16.create_csv_file()
        file_size: str = '{:.3f}'.format(create_csv_obj_16.get_file_size_kb())
        self.assertEqual(file_size, '0.000')
        file_checksum: str = create_csv_obj_16.get_file_checksum()
        self.assertEqual(file_checksum, '')

    def test_csv_017(self):
        file_path: str = 'test_csv_tables/table_17.csv'
        # headers tuple has 7 elements, and the nested tuples have 6 elements.
        table_data: tuple = tuple((tuple(range(6))) for _ in range(50))
        create_csv_obj_17 = CsvFileWithTable(file_path, table_data)
        with self.assertRaises(ValueError):
            create_csv_obj_17.create_csv_file()
        file_size: str = '{:.3f}'.format(create_csv_obj_17.get_file_size_kb())
        self.assertEqual(file_size, '0.000')
        file_checksum: str = create_csv_obj_17.get_file_checksum()
        self.assertEqual(file_checksum, '')

    def test_csv_018(self):
        """
        We indicate the wrong path to the directory: the wrong directory should not be created, just like the file
        """
        file_path: str = 'fail_path/test_table_1.csv'
        table_headers: tuple = ('column_1',)
        table_data: tuple = (('1',),)
        create_csv_obj_18 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
        with self.assertRaises(FileNotFoundError):
            create_csv_obj_18.create_csv_file()
        self.assertFalse(path.exists(file_path))

        file_size: str = '{:.3f}'.format(create_csv_obj_18.get_file_size_kb())
        self.assertEqual(file_size, '0.000')

        file_checksum: str = create_csv_obj_18.get_file_checksum()
        self.assertEqual(file_checksum, '')

    def test_csv_019(self):
        file_path: str = 'fail_path/test_table_1.csv'
        table_data: tuple = tuple((tuple(range(7))) for _ in TestCreateCSV.tuple_of_500)
        create_csv_obj_19 = CsvFileWithTable(file_path, table_data)
        with self.assertRaises(FileNotFoundError):
            create_csv_obj_19.create_csv_file()
        self.assertFalse(path.exists(file_path))

        file_size: str = '{:.3f}'.format(create_csv_obj_19.get_file_size_kb())
        self.assertEqual(file_size, '0.000')

        file_checksum: str = create_csv_obj_19.get_file_checksum()
        self.assertEqual(file_checksum, '')

    def test_csv_020(self):
        file_path: str = 'fail_path/path_to_csv/test_table_2.csv'
        table_data: tuple = tuple((tuple(range(7))) for _ in TestCreateCSV.tuple_of_500)
        create_csv_obj_20 = CsvFileWithTable(file_path, table_data)
        with self.assertRaises(FileNotFoundError):
            create_csv_obj_20.create_csv_file()
        self.assertFalse(path.exists(file_path))

        file_size: str = '{:.3f}'.format(create_csv_obj_20.get_file_size_kb())
        self.assertEqual(file_size, '0.000')

        file_checksum: str = create_csv_obj_20.get_file_checksum()
        self.assertEqual(file_checksum, '')

    def test_csv_021(self):
        file_path: str = 'test_table_3.csv'
        table_data: tuple = tuple((tuple(range(7))) for _ in TestCreateCSV.tuple_of_500)
        create_csv_obj_21 = CsvFileWithTable(file_path, table_data)
        with self.assertRaises(FileNotFoundError):
            create_csv_obj_21.create_csv_file()
        self.assertFalse(path.exists(file_path))

        file_size: str = '{:.3f}'.format(create_csv_obj_21.get_file_size_kb())
        self.assertEqual(file_size, '0.000')

        file_checksum: str = create_csv_obj_21.get_file_checksum()
        self.assertEqual(file_checksum, '')

    def test_csv_022(self):
        file_path: str = ''
        table_data: tuple = tuple((tuple(range(7))) for _ in TestCreateCSV.tuple_of_500)
        create_csv_obj_22 = CsvFileWithTable(file_path, table_data)
        with self.assertRaises(FileNotFoundError):
            create_csv_obj_22.create_csv_file()
        self.assertFalse(path.exists(file_path))

        file_size: str = '{:.3f}'.format(create_csv_obj_22.get_file_size_kb())
        self.assertEqual(file_size, '0.000')

        file_checksum: str = create_csv_obj_22.get_file_checksum()
        self.assertEqual(file_checksum, '')

    def test_csv_023(self):
        """ Use of other languages """
        file_path: str = 'test_csv_tables/test_table_23.csv'
        table_data: tuple = tuple((tuple(range(7))) for _ in range(10))
        create_csv_obj_23 = CsvFileWithTable(file_path, table_data, lang='es')
        create_csv_obj_23.create_csv_file()
        self.assertTrue(path.exists(file_path))

        file_size: str = '{:.3f}'.format(create_csv_obj_23.get_file_size_kb())
        self.assertEqual(file_size, '0.227')

        file_checksum: str = create_csv_obj_23.get_file_checksum()
        self.assertEqual(file_checksum, 'c4c8eaa9694e7358d43dc1b45366da65d5047b92435ee685295dbc107fdd39b4')

    def test_csv_024(self):
        """ Specifying the wrong value for the language """
        file_path: str = 'test_csv_tables/test_table_24.csv'
        table_data: tuple = tuple((tuple(range(7))) for _ in range(5))
        create_csv_obj_24 = CsvFileWithTable(file_path, table_data, lang='00')
        create_csv_obj_24.create_csv_file()
        self.assertTrue(path.exists(file_path))

        file_size: str = '{:.3f}'.format(create_csv_obj_24.get_file_size_kb())
        self.assertEqual(file_size, '0.115')

        file_checksum: str = create_csv_obj_24.get_file_checksum()
        self.assertEqual(file_checksum, '2a7ec97cf1add970cf9abc148111abc83d1eae8fbdf68e6b7c57232988cbd666')

    def test_csv_025(self):
        file_path: str = 'test_csv_tables/test_table_25.csv'
        table_data: tuple = tuple((tuple(range(7))) for _ in range(3))
        create_csv_obj_25 = CsvFileWithTable(file_path, table_data, lang='is')
        create_csv_obj_25.create_csv_file()
        self.assertTrue(path.exists(file_path))

        file_size: str = '{:.3f}'.format(create_csv_obj_25.get_file_size_kb())
        self.assertEqual(file_size, '0.108')

        file_checksum: str = create_csv_obj_25.get_file_checksum()
        self.assertEqual(file_checksum, 'd67805e2f1963c29b752c18a5c4f916e1c2e381d211c45bfab9eabc0cc3996a8')

    def test_csv_026(self):
        file_path: str = 'test_csv_tables/test_table_26.csv'
        table_data: tuple = tuple((tuple(range(7))) for _ in range(3))
        create_csv_obj_26 = CsvFileWithTable(file_path, table_data, lang='ru')
        create_csv_obj_26.create_csv_file()
        self.assertTrue(path.exists(file_path))

        file_size: str = '{:.3f}'.format(create_csv_obj_26.get_file_size_kb())
        self.assertEqual(file_size, '0.146')

        file_checksum: str = create_csv_obj_26.get_file_checksum()
        self.assertEqual(file_checksum, '46cafb0c19521581e1a3edac0f921dc57e88a9e89389a7fd1e7e1b17f918b8a6')

    def test_csv_027(self):
        """ Checking the default language """
        table_data: tuple = tuple((tuple(range(7))) for _ in range(3))

        file_path_1: str = 'test_csv_tables/test_table_27_1.csv'
        create_csv_obj_27_1 = CsvFileWithTable(file_path_1, table_data)
        create_csv_obj_27_1.create_csv_file()
        self.assertTrue(path.exists(file_path_1))
        file_size_1: str = '{:.3f}'.format(create_csv_obj_27_1.get_file_size_kb())
        self.assertEqual(file_size_1, '0.097')
        file_checksum_1: str = create_csv_obj_27_1.get_file_checksum()
        self.assertEqual(file_checksum_1, '2f76ced0522e538ac823b6f49453f248f8c65fff2bebee77f26bd2b355709319')

        file_path_2: str = 'test_csv_tables/test_table_27_2.csv'
        create_csv_obj_27_2 = CsvFileWithTable(file_path_2, table_data, lang='en')
        create_csv_obj_27_2.create_csv_file()
        self.assertEqual(path.exists(file_path_2), True)
        file_size_2: str = '{:.3f}'.format(create_csv_obj_27_2.get_file_size_kb())
        self.assertEqual(file_size_1, file_size_2)
        file_checksum_2: str = create_csv_obj_27_2.get_file_checksum()
        self.assertEqual(file_checksum_1, file_checksum_2)

    def test_csv_028(self):
        """ Checking that specifying the language will not break custom table headers """
        file_path: str = 'test_csv_tables/test_table_28.csv'
        table_data: tuple = tuple((tuple(range(15))) for _ in range(3))
        table_headers: tuple = tuple('___' for _ in range(15))

        create_csv_obj_28 = CsvFileWithTable(file_path, table_data, table_headers=table_headers, lang='es')
        create_csv_obj_28.create_csv_file()

        self.assertTrue(path.exists(file_path))
        file_size: str = '{:.3f}'.format(create_csv_obj_28.get_file_size_kb())
        self.assertEqual(file_size, '0.165')
        file_checksum: str = create_csv_obj_28.get_file_checksum()
        self.assertEqual(file_checksum, 'a76a624def64f20303cbfc22ce95a77b8c79a92ca02acc079fc74291d618ac01')

    def test_csv_029(self):
        file_path: str = 'test_csv_tables/73de7a80-b9fe-4534-be66-468d64e2d5bf.csv'
        table_headers: tuple = ('column_1', 'column_2')
        table_data: tuple = (('1', '2'), ('1', '2'))
        create_csv_obj_29 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
        create_csv_obj_29.create_csv_file()
        self.assertTrue(path.exists(file_path))

        file_size: str = '{:.3f}'.format(create_csv_obj_29.get_file_size_kb())
        self.assertEqual(file_size, '0.028')

        file_checksum: str = create_csv_obj_29.get_file_checksum()
        self.assertEqual(file_checksum, '323179bc81bff55700949e4887293a16a743c2dcbf1d76f7cb062e2b3ad58cc4')

    def test_csv_030(self):
        file_path: str = 'test_csv_tables/31d2e7ab-8497-4b7e-8b51-09ba36665552.csv'
        table_headers: tuple = ('column_1', 'column_2', 'column_3', 'column_4', 'column_5')
        table_data: tuple = (('1', '2', '3', '4', '5'),)
        create_csv_obj_30 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
        create_csv_obj_30.create_csv_file()
        self.assertTrue(path.exists(file_path))

        file_size: str = '{:.3f}'.format(create_csv_obj_30.get_file_size_kb())
        self.assertEqual(file_size, '0.056')

        file_checksum: str = create_csv_obj_30.get_file_checksum()
        self.assertEqual(file_checksum, '415e456d6d95687cf868df2d3f7dbe5e01b52e186f40b1dda78a9d07482be845')

    def test_csv_031(self):
        file_path: str = 'test_csv_tables/615db441-f6b3-4799-ae2e-aab855561d16.csv'
        table_headers: tuple = ('_',)
        table_data: tuple = (('&',),)
        create_csv_obj_31 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
        create_csv_obj_31.create_csv_file()
        self.assertTrue(path.exists(file_path))

        file_size: str = '{:.3f}'.format(create_csv_obj_31.get_file_size_kb())
        self.assertEqual(file_size, '0.006')

        file_checksum: str = create_csv_obj_31.get_file_checksum()
        self.assertEqual(file_checksum, '52767a1ae5126da2adc66b2fe25341d9157946c2c6f59afb71af5c2944730de6')

    def test_csv_032(self):
        """ Checking that the file does not exist after invalid data validation """
        file_path: str = 'test_csv_tables/0ce8e383-3a09-4e9d-bc18-9f82e3fc2748.csv'
        table_headers: tuple = ('123', '123', '')
        table_data: tuple = (('1', '2', '3'),)
        create_csv_obj_32 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
        with self.assertRaises(ValueError):
            create_csv_obj_32.create_csv_file()
        file_size: str = '{:.3f}'.format(create_csv_obj_32.get_file_size_kb())
        self.assertEqual(file_size, '0.000')
        file_checksum: str = create_csv_obj_32.get_file_checksum()
        self.assertEqual(file_checksum, '')

    def test_csv_033(self):
        for i in range(1, 1_250):
            group_uuid: str = str(uuid4())
            file_path: str = f'test_csv_tables/{i}_{group_uuid}.csv'
            table_headers: tuple = ('_', 'qwerty')
            table_data: tuple = (('&', '%'),)
            create_csv_obj_33 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
            create_csv_obj_33.create_csv_file()
            self.assertTrue(path.exists(file_path))

            wrong_group_uuid: str = str(uuid4())
            wrong_path: str = f'test_csv_tables/{i}_{wrong_group_uuid}.csv'
            self.assertFalse(path.exists(wrong_path))

            file_size: str = '{:.3f}'.format(create_csv_obj_33.get_file_size_kb())
            self.assertEqual(file_size, '0.015')

            file_checksum: str = create_csv_obj_33.get_file_checksum()
            self.assertEqual(file_checksum, '84d78b707c8ca6b18bee74aad7540016d50b688dd516a6a28e3e861f51a7a697')

    def test_csv_034(self):
        """ 10 headers and 1_000_000 rows """
        group_id: int = randint(100, 1_000)
        group_uuid: str = str(uuid4())
        file_path: str = f'test_csv_tables/{group_id}_{group_uuid}.csv'
        table_headers: tuple = tuple(f'column_{i}' for i in range(10))
        table_data: tuple = tuple((tuple(range(10))) for _ in range(1_000_000))
        create_csv_obj_34 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
        create_csv_obj_34.create_csv_file()
        self.assertTrue(path.exists(file_path))

        file_size: str = '{:.3f}'.format(create_csv_obj_34.get_file_size_kb())
        self.assertEqual(file_size, '20507.901')

        file_checksum: str = create_csv_obj_34.get_file_checksum()
        self.assertEqual(file_checksum, '046b17aedb854fcb48ecd8183e214af27db8fb4d8edb15394acbf23831a1ef94')

    def test_csv_035(self):
        """ Check for file overwriting if the same table is generated 100 times with different data """
        iters: int = 100

        group_id: int = randint(100, 1_000)
        group_uuid: str = str(uuid4())
        file_path: str = f'test_csv_tables/{group_id}_{group_uuid}.csv'

        hash_vault: list = []  # {hash: size, ...}

        for _iter in range(iters):
            seed()  # This sets the seed based on the current time.
            _rand_int: int = randint(1, 100)
            rand_str: str = ''.join(choice(ascii_letters + digits) for _ in range(_rand_int))

            table_headers: tuple = tuple(rand_str for _ in range(_rand_int))
            table_data: tuple = tuple((tuple(rand_str for _ in range(_rand_int))) for _ in range(25))

            create_csv_obj_35 = CsvFileWithTable(file_path, table_data, table_headers=table_headers)
            create_csv_obj_35.create_csv_file()
            self.assertTrue(path.exists(file_path), f'iter = {_iter}')

            file_size: str = '{:.3f}'.format(create_csv_obj_35.get_file_size_kb())
            self.assertTrue(len(file_size) > 0, len(file_size))

            file_checksum: str = create_csv_obj_35.get_file_checksum()
            hash_vault.append(file_checksum)

        # we check that the number of keys = iters
        keys: int = len(hash_vault)
        self.assertEqual(keys, iters, f'keys = {keys}')


if __name__ == '__main__':
    unittest.main()
