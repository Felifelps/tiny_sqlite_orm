import unittest
from tests.fixtures import TestCaseWithTables


class TestQueryset(TestCaseWithTables):

    def setUp(self):
        self.queryset = self.table_with_id.objects
        return super().setUp()

    def check_select_query(self, expected_query, **select_args):
        query = self.queryset.select(**select_args)
        self.assertEqual(
            expected_query,
            str(query)
        )

    def test_select_all(self):
        self.check_select_query('SELECT * FROM withid WHERE 1;')

    def test_select_equal(self):
        self.check_select_query(
            'SELECT * FROM withid WHERE username = \'User1\';',
            username='User1',
        )

    def test_select_not_equal(self):
        self.check_select_query(
            'SELECT * FROM withid WHERE username <> \'User1\';',
            username__ne='User1',
        )

    def test_select_greater_filters(self):
        self.check_select_query(
            'SELECT * FROM withid WHERE id > 1 AND id >= 1;',
            id__gt=1,
            id__ge=1,
        )

    def test_select_less_filters(self):
        self.check_select_query(
            'SELECT * FROM withid WHERE id < 1 AND id <= 1;',
            id__lt=1,
            id__le=1,
        )

    def test_select_in(self):
        self.check_select_query(
            'SELECT * FROM withid WHERE username IN (\'User1\', \'User2\');',
            username__in=['User1', 'User2']
        )

    def test_select_contains_and_icontains(self):
        self.check_select_query(
            'SELECT * FROM withid WHERE instr(username, \'1\') > 0 AND username LIKE lower(\'%User%\');',
            username__contains='1',
            username__icontains='User',
        )

    def test_aggregate_functions(self):
        print(list(self.queryset.select()))
        self.assertEqual(self.queryset.count(), 0)
        self.assertEqual(self.queryset.sum(column='id'), 0)
        self.assertEqual(self.queryset.max(column='id'), 0)
        self.assertEqual(self.queryset.min(column='id'), 0)
        self.assertEqual(self.queryset.avg(column='id'), 0)

if __name__ == '__main__':
    unittest.TestLoader.sortTestMethodsUsing = None
    unittest.main()
