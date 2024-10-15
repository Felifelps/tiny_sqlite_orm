import unittest
from tests.fixtures import TestCaseWithDatabase
from tiny_sqlite_orm import (
    TextField, IntegerField, BooleanField,
    DateField, Table, AutoField, ForeignKeyField
)
from datetime import date


class TestUserTableCreation(TestCaseWithDatabase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Table.db = cls.db

    def test_create_simple_table(self):
        class User(Table):
            id = AutoField(primary_key=True)
            username = TextField(unique=True)
            active = BooleanField(default=True)

        self.db.create_tables_if_not_exists([User])

        expected_schema = (
            'CREATE TABLE IF NOT EXISTS user '
            '(id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'username TEXT UNIQUE, active BOOLEAN DEFAULT TRUE);'
        )
        self.assertEqual(User._schema, expected_schema)

    def test_create_table_with_date(self):
        class Event(Table):
            id = AutoField(primary_key=True)
            name = TextField(unique=True)
            event_date = DateField(auto_today=True)

        self.db.create_tables_if_not_exists([Event])

        expected_schema = (
            'CREATE TABLE IF NOT EXISTS event '
            '(id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'name TEXT UNIQUE, event_date TEXT DEFAULT \'{}\');'
        ).format(date.today().isoformat())
        self.assertEqual(Event._schema, expected_schema)

    def test_create_table_with_integer_field(self):
        class Product(Table):
            id = AutoField(primary_key=True)
            name = TextField(unique=True)
            quantity = IntegerField(default=0)

        self.db.create_tables_if_not_exists([Product])

        expected_schema = (
            'CREATE TABLE IF NOT EXISTS product '
            '(id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'name TEXT UNIQUE, quantity INTEGER DEFAULT 0);'
        )
        self.assertEqual(Product._schema, expected_schema)

    def test_foreign_key_table_creation(self):
        class Category(Table):
            id = AutoField(primary_key=True)
            name = TextField(unique=True)

        class Item(Table):
            id = AutoField(primary_key=True)
            name = TextField(unique=True)
            category = ForeignKeyField(ref_table=Category)

        self.db.create_tables_if_not_exists([Category, Item])

        expected_item_schema = (
            'CREATE TABLE IF NOT EXISTS item '
            '(id INTEGER PRIMARY KEY AUTOINCREMENT, '
            'name TEXT UNIQUE, category INTEGER, '
            'FOREIGN KEY (category) REFERENCES category(id));'
        )
        self.assertEqual(Item._schema, expected_item_schema)

    def test_insert_into_user_table(self):
        class User(Table):
            id = AutoField(primary_key=True)
            username = TextField(unique=True)
            active = BooleanField(default=True)

        self.db.create_tables_if_not_exists([User])

        user_data = {'username': 'testuser'}
        user = User.create(**user_data)

        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.active)


if __name__ == '__main__':
    unittest.main()
