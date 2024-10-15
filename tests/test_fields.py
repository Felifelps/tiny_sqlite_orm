import unittest
from tests.fixtures import TestCaseWithTables
from tiny_sqlite_orm.field import (
    IntegerField, AutoField, TextField, CharField,
    BooleanField, DateField, DatetimeField, ForeignKeyField
)
from datetime import date, datetime


class TestFieldTypes(TestCaseWithTables):

    @classmethod
    def setUpClass(cls):
        cls.mock_table = cls.create_table(
            'MockTable',
            {
                'id': AutoField(primary_key=True),
                'username': TextField(unique=True),
            }
        )
        cls.create_tables_on_db([cls.mock_table])

    def test_integer_field(self):
        field = IntegerField()
        self.assertEqual(field._type, 'INTEGER')
        self.assertEqual(field._python_type, int)
        field._check_field_value(42)  # Valid
        with self.assertRaises(ValueError):
            field._check_field_value("NotAnInt")  # Invalid

    def test_auto_field(self):
        field = AutoField(primary_key=True)
        self.assertTrue(field.primary_key)
        self.assertEqual(field._type, 'INTEGER')
        self.assertEqual(field._python_type, int)

    def test_text_field(self):
        field = TextField()
        self.assertEqual(field._type, 'TEXT')
        self.assertEqual(field._python_type, str)
        field._check_field_value("SampleText")  # Valid
        with self.assertRaises(ValueError):
            field._check_field_value(None)  # Invalid

    def test_char_field(self):
        field = CharField(max_length=10)
        self.assertEqual(field._type, 'VARCHAR(10)')
        field._check_field_value("ShortText")  # Valid
        with self.assertRaises(ValueError):
            field._check_field_value("TooLongText")  # Invalid due to length

    def test_boolean_field(self):
        field = BooleanField()
        self.assertEqual(field._type, 'BOOLEAN')
        self.assertEqual(field._python_type, bool)
        field._check_field_value(True)  # Valid
        field._check_field_value('')  # Valid
        field._check_field_value(123)  # Valid

    def test_date_field(self):
        field = DateField()
        self.assertEqual(field._type, 'TEXT')
        today = date.today()
        field._check_field_value(today.isoformat())  # Valid
        with self.assertRaises(ValueError):
            field._check_field_value("InvalidDate")  # Invalid

    def test_datetime_field(self):
        field = DatetimeField()
        self.assertEqual(field._type, 'TEXT')
        now = datetime.now()
        field._check_field_value(now.isoformat())  # Valid
        with self.assertRaises(ValueError):
            field._check_field_value("InvalidDatetime")  # Invalid

    def test_foreign_key_field(self):
        field = ForeignKeyField(self.mock_table)
        self.assertEqual(field._type, 'INTEGER')
        self.assertEqual(field._python_type, int)


if __name__ == '__main__':
    unittest.main()
