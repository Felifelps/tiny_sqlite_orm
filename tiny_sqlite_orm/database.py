import sqlite3


class Database:

    def __init__(self, database_name):
        self._conn = sqlite3.connect(database_name)
        self.__set_foreign_keys()

    def __set_foreign_keys(self):
        self._conn.execute('PRAGMA foreign_keys = ON;')

    def create_tables_if_not_exists(self, tables):
        for table in tables:
            table._initialize_and_create_table(self)

    def disconnect(self):
        self._conn.close()
