import unittest
from tests.fixtures import DatabaseTestCase
from tiny_sqlite_orm.table import Table
from tiny_sqlite_orm.field import TextField, IntegerField


class TestTable(DatabaseTestCase):

    def setUp(self):
        self.table = type(
            'User',
            (Table, ),
            {'name': TextField(unique=True),
             'age': IntegerField(),
             'db': self.db}
        )
        self.db.create_tables_if_not_exists([self.table])

    def test_a_create_user(self):
        user = self.table.create(name="John", age=30)
        self.assertEqual(user.name, "John")
        self.assertEqual(user.age, 30)

    def test_b_select_user(self):
        user = self.__get_test_user()
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "John")

    def __get_test_user(self):
        return self.table.objects.select(name="John").first()

    def test_c_update_user(self):
        user = self.__get_test_user()
        user.age = 31
        user.save()
        updated_user = self.__get_test_user()
        self.assertEqual(updated_user.age, 31)

    def test_d_delete_user(self):
        user = self.__get_test_user()
        user.delete()
        deleted_user = self.__get_test_user()
        self.assertIsNone(deleted_user)

if __name__ == '__main__':
    unittest.main()
