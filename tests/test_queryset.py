import unittest
from tests.fixtures import TestCaseWithTables
from tiny_sqlite_orm import CharField, IntegerField


unittest.TestLoader.sortTestMethodsUsing = None

class TestQueryset(TestCaseWithTables):

    @classmethod
    def setUpClass(cls):
        table = cls.create_table(
            'QuerysetTesting',
            {
                'username': CharField(max_length=50),
                'age': IntegerField()
            }
        )
        cls.create_tables_on_db([table])
        cls.user1 = table.create(username='User1', age=30)
        cls.user2 = table.create(username='user2', age=50)
        cls.queryset = table.objects

    def check_select_query(self, expected_query, **select_args):
        query = self.queryset.select(**select_args)
        self.assertEqual(expected_query, str(query))
        return query

    def test_select_all(self):
        query = self.check_select_query(
            'SELECT * FROM querysettesting WHERE 1;'
        )
        self.check_if_query_matches_all_users(query)

    def check_if_query_matches_all_users(self, query):
        self.assertDictEqual(query.first().attrs, self.user1.attrs)
        self.assertDictEqual(query.last().attrs, self.user2.attrs)

    def test_select_equal(self):
        query = self.check_select_query(
            'SELECT * FROM querysettesting WHERE username = \'User1\';',
            username='User1',
        )
        self.assertDictEqual(query.first().attrs, self.user1.attrs)

    def test_select_not_equal(self):
        query = self.check_select_query(
            'SELECT * FROM querysettesting WHERE username <> \'User1\';',
            username__ne='User1',
        )
        self.assertDictEqual(query.first().attrs, self.user2.attrs)

    def test_select_greater_filters(self):
        query = self.check_select_query(
            'SELECT * FROM querysettesting WHERE age > 20 AND age >= 30;',
            age__gt=20,
            age__ge=30,
        )
        self.check_if_query_matches_all_users(query)

    def test_select_less_filters(self):
        query = self.check_select_query(
            'SELECT * FROM querysettesting WHERE age < 60 AND age <= 50;',
            age__lt=60,
            age__le=50,
        )
        self.check_if_query_matches_all_users(query)

    def test_select_in(self):
        query = self.check_select_query(
            'SELECT * FROM querysettesting WHERE username IN (\'User1\', \'user2\');',
            username__in=['User1', 'user2']
        )
        self.check_if_query_matches_all_users(query)

    def test_select_contains_and_icontains(self):
        contains_query = self.check_select_query(
            'SELECT * FROM querysettesting WHERE instr(username, \'User\') > 0;',
            username__contains='User',
        )
        icontains_query = self.check_select_query(
            'SELECT * FROM querysettesting WHERE username LIKE lower(\'%User%\');',
            username__icontains='User',
        )

        self.assertDictEqual(contains_query.first().attrs, self.user1.attrs)
        self.check_if_query_matches_all_users(icontains_query)

    def test_aggregate_functions(self):
        self.assertEqual(self.queryset.count(), 2)
        self.assertEqual(self.queryset.sum('age'), 80)
        self.assertEqual(self.queryset.max('age'), 50)
        self.assertEqual(self.queryset.min('age'), 30)
        self.assertEqual(self.queryset.avg('age'), 40)

    def test_update(self):
        expected_update_query = 'UPDATE querysettesting SET username = \'User2\' WHERE username = \'user2\';'
        query = self.queryset.update(
            {'username': 'User2'},
            username='user2'
        )
        updated_user2 = self.queryset.select(id=self.user2.id).first()

        self.assertEqual(str(query), expected_update_query)
        self.assertEqual(updated_user2.username, 'User2')

    def test_z_delete(self):
        # Named "test_z" for become the last test

        expected_delete_query = 'DELETE FROM querysettesting WHERE username = \'User2\';'
        query = self.queryset.delete(
            username='User2'
        )
        deleted_user2 = self.queryset.select(id=self.user2.id).first()

        self.assertEqual(str(query), expected_delete_query)
        self.assertIsNone(deleted_user2)

if __name__ == '__main__':
    unittest.main()
