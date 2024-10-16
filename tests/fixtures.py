import unittest
from tiny_sqlite_orm import Database, Table


class TestCaseWithDatabase(unittest.TestCase):

    db = Database(':memory:')

    @classmethod
    def tearDownClass(cls):
        cls.db.disconnect()


class TestCaseWithTables(TestCaseWithDatabase):

    tables = None

    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()

    @classmethod
    def tearDownClass(cls):
        for table in cls.tables:
            cls.db._conn.execute(f'DELETE FROM {table.table_name} WHERE 1;')
        cls.db._conn.commit()

    @classmethod
    def create_tables_on_db(cls, tables):
        cls.db.create_tables_if_not_exists(tables)
        cls.tables = tables

    @classmethod
    def create_table(cls, name, fields):
        return type(
            name,
            (Table,),
            {**fields}
        )
