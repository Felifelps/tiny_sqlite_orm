from datetime import date


class Utils:

    gen_query_by_descriptor_functions = {
        'lt': '{column} < {value}',
        'le': '{column} <= {value}',
        'gt': '{column} > {value}',
        'ge': '{column} >= {value}',
        'ne': '{column} <> {value}',
        'contains': 'instr({column}, {value}) > 0',
        'icontains': '{column} LIKE \'%{raw_value}%\''
    }

    def convert_to_sql_type(value):
        if isinstance(value, bool):
            return 'TRUE' if value else 'FALSE'
        
        if value is None:
            return 'NULL'

        if isinstance(value, str) or isinstance(value, date):
            return f'\'{value}\''

        return str(value)

    def format_iterable_as_sql_tuple(items):
        return f"({', '.join(items)})"

    def convert_values_to_sql_safe_format(values):
        return map(
            Utils.convert_to_sql_type,
            values
        )

    def parse_fields_for_insert(**fields):
        if not fields:
            return 'DEFAULT', ''
        columns = Utils.format_iterable_as_sql_tuple(fields.keys())
        values = Utils.format_iterable_as_sql_tuple(
            Utils.convert_values_to_sql_safe_format(fields.values())
        )
        return columns, values

    def parse_fields_for_update(**fields):
        return ', '.join(
            [f'{column} = {Utils.convert_to_sql_type(value)}' for column, value in fields.items()]
        )

    def get_where_from_query(query_descriptor, value):
        query_descriptor = query_descriptor.split('__')

        column = query_descriptor[0]
        where_text = '{column} = {value}'
        if len(query_descriptor) > 1:
            where_text = Utils.gen_query_by_descriptor_functions.get(
                query_descriptor[-1]
            )

        if '{raw_value}' in where_text:
            return where_text.format(
                column=column,
                raw_value=value
            )

        return where_text.format(
            column=column,
            value=Utils.convert_to_sql_type(value)
        )
        
