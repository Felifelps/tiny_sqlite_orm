import os
import platform
import unittest
from tiny_sqlite_orm import Database, Table, TextField


class TestCaseWithDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db = Database('test_database.db')

    @classmethod
    def tearDownClass(cls):
        cls.db.disconnect()
        cls.__delete_database_if_exists()

    def __delete_database_if_exists():
        command = 'rm -f {}'
        if platform.system() == 'Windows':
            command = 'del /f /q {}'

        os.system(command.format('test_database.db'))


class TestCaseWithTables(TestCaseWithDatabase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.table_with_pk = cls.create_table(
            name='WithPk',
            fields={'username': TextField(primary_key=True)}
        )
        cls.table_with_id = cls.create_table(
            name='WithId',
            fields={'username': TextField(unique=True)}
        )
        cls.db.create_tables_if_not_exists([
            cls.table_with_pk,
            cls.table_with_id
        ])

    @classmethod
    def create_table(cls, name, fields):
        attrs = {**fields, 'db': cls.db}
        return type(name, (Table,), attrs)
