import unittest
from tests.fixtures import TestCaseWithTables


class TestTable(TestCaseWithTables):

    def test_primary_key(self):
        self.assertIs(self.table_with_pk.pk, self.table_with_pk.username)
        self.assertIs(self.table_with_id.pk, self.table_with_id.id)

    def test_create_user_with_pk(self):
        attrs = {'username': 'User1'}
        user = self.table_with_pk.create(**attrs)
        self.assertIsNotNone(user, 'User not created with PK')
        self.assertDictEqual(user.attrs, attrs)

    def test_create_user_with_auto_id(self):
        attrs = {'username': 'User1'}
        user = self.table_with_id.create(**attrs)
        self.assertIsNotNone(user, 'User not created with auto ID')
        self.assertDictEqual(user.attrs, {**attrs, 'id': 1})

    def test_schema_generation(self):
        expected_pk_schema = 'CREATE TABLE IF NOT EXISTS withpk (username TEXT PRIMARY KEY);'
        expected_id_schema = 'CREATE TABLE IF NOT EXISTS withid (username TEXT UNIQUE, id INTEGER PRIMARY KEY AUTOINCREMENT);'

        self.assertEqual(self.table_with_pk._schema, expected_pk_schema)
        self.assertEqual(self.table_with_id._schema, expected_id_schema)

if __name__ == '__main__':
    unittest.TestLoader.sortTestMethodsUsing = None
    unittest.main()
