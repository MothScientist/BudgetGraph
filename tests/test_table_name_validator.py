import unittest

from budget_control.main.validators.table_name import table_name_validation


class TestTableNameValidator(unittest.TestCase):
    def test_table_name_validator_1(self):
        res = table_name_validation("budget_1")
        self.assertEqual(res, True)

    def test_table_name_validator_2(self):
        res = table_name_validation("budget_01")
        self.assertEqual(res, False)

    def test_table_name_validator_3(self):
        res = table_name_validation("budget_100")
        self.assertEqual(res, True)

    def test_table_name_validator_4(self):
        res = table_name_validation("budjet_10")
        self.assertEqual(res, False)

    def test_table_name_validator_5(self):
        res = table_name_validation("bubget_1")
        self.assertEqual(res, False)

    def test_table_name_validator_6(self):
        res = type(table_name_validation("bubget_1"))
        self.assertEqual(res, bool)

    def test_table_name_validator_7(self):
        res = type(table_name_validation("budget_100"))
        self.assertEqual(res, bool)


if __name__ == '__main__':
    unittest.main()
