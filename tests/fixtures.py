import os
import platform
import unittest
from tiny_sqlite_orm import Database


class DatabaseTestCase(unittest.TestCase):

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
