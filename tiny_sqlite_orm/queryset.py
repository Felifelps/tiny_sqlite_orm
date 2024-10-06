from .record import Record
from .field import AutoField
from .utils import Utils


class Queryset:

    def __init__(self, table, data=[], last_instruction=''):
        self.table = table
        self.__data = data
        self.__last_instruction = last_instruction
        self.__current_index = 0

    def __str__(self):
        return self.__last_instruction

    def __iter__(self):
        return self

    def __next__(self):
        if self.__current_index < len(self.__data):
            value = self.__data[self.__current_index]
            self.__current_index += 1
            return value

        self.__current_index = 0
        raise StopIteration

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.__data[index]
        raise TypeError("Invalid Argument Type")

    def first(self):
        return self.__get_item_or_none(0)

    def last(self):
        return self.__get_item_or_none(-1)

    def __get_item_or_none(self, index):
        if len(self.__data):
            return self.__data[index]
        return None

    @property
    def columns(self):
        return (field._name for field in self.table.get_fields())

    def count(self, **query):
        return self.__aggregate_function('COUNT', '*', query)

    def sum(self, column, **query):
        return self.__aggregate_function('SUM', column, query)

    def avg(self, column, **query):
        return self.__aggregate_function('AVG', column, query)

    def max(self, column, **query):
        return self.__aggregate_function('MAX', column, query)

    def min(self, column, **query):
        return self.__aggregate_function('MIN', column, query)

    def __aggregate_function(self, function, column, query):
        where = self.__get_where_clause_by_query(query)
        return self.__execute(
            f'SELECT {function}({column}) FROM {{table_name}} WHERE {where};',
            format_function=lambda result: tuple(result)[0][0] or 0,
        )

    def __get_where_clause_by_query(self, query):
        if not query:
            return '1'

        where = []
        if ('SELECT' in self.__last_instruction and
            'WHERE' in self.__last_instruction):
            earlier_where = self.__last_instruction.split(
                'WHERE '
            )[-1].replace(';', '')
            where.append(earlier_where)

        where.extend(
            Utils.get_where_from_query(
                descriptor, value
            ) for descriptor, value in query.items()
        )
        return ' AND '.join(where)

    def __execute(self, instruction, format_function=None):
        instruction = instruction.format(table_name=self.table.table_name)
        result = self.table.db._conn.execute(instruction)
        self.table.db._conn.commit()

        if format_function is not None:
            return format_function(result)
        else:
            data = [
                self.__gen_record_by_query_result(
                    record
                ) for record in result
            ]

        return Queryset(
            self.table,
            data=data,
            last_instruction=instruction
        )

    def __gen_record_by_query_result(self, record):
        index = 0
        attrs = {}
        for field in self.table.get_fields():
            attrs[field._name] = field._convert_sql_value_to_python(
                record[index]
            )
            index += 1

        return Record(
            self.table,
            **attrs
        )

    def select(self, **query):
        where = self.__get_where_clause_by_query(query)
        return self.__execute(
            f'SELECT * FROM {{table_name}} WHERE {where};'
        )

    def update(self, fields, **query):
        where = self.__get_where_clause_by_query(query)
        fields = Utils.parse_fields_for_update(**fields)

        return self.__execute(
            f'UPDATE {{table_name}} SET {fields} WHERE {where};'
        )

    def delete(self, **query):
        where = self.__get_where_clause_by_query(query)
        return self.__execute(f'DELETE FROM {{table_name}} WHERE {where};')

    def insert(self, **fields):
        self.__validate_and_format_insert_fields(fields)
        columns, values = Utils.parse_fields_for_insert(**fields)

        return self.__execute(
            f'INSERT INTO {{table_name}} {columns} VALUES {values};',
            format_function=lambda _: self.__create_record_from_insert(fields)
        )

    def __validate_and_format_insert_fields(self, fields):
        for field in self.table.get_fields():
            if isinstance(field, AutoField):
                continue

            if field._name not in fields:
                self.__set_to_default_value(field, fields)

            value = fields[field._name]

            field._check_field_value(value)

            fields[field._name] = value

    def __set_to_default_value(self, field, fields):
        fields[field._name] = field.default

    def __create_record_from_insert(self, fields):
        query = self.select(**fields)
        return query.last()
