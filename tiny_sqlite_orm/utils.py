from datetime import date


class Utils:

    gen_query_by_descriptor_functions = {
        'lt': '{column} < {value}',
        'le': '{column} <= {value}',
        'gt': '{column} > {value}',
        'ge': '{column} >= {value}',
        'ne': '{column} <> {value}',
        'in': '{column} IN {value_as_tuple}',
        'contains': 'instr({column}, {value}) > 0',
        'icontains': '{column} LIKE lower(\'%{raw_value}%\')'
    }

    def convert_to_sql_type(value):
        if isinstance(value, bool):
            return 'TRUE' if value else 'FALSE'
        
        if value is None:
            return 'NULL'

        if isinstance(value, str) or isinstance(value, date):
            return f'\'{value}\''

        return str(value)

    def format_as_sql_columns_tuple(items):
        return f"({', '.join(items)})"

    def format_as_sql_values_tuple(items):
        items = map(
            Utils.convert_to_sql_type,
            items
        )
        return f"({', '.join(items)})"

    def parse_fields_for_insert(**fields):
        if not fields:
            return 'DEFAULT', ''
        columns = Utils.format_as_sql_columns_tuple(fields.keys())
        values = Utils.format_as_sql_values_tuple(fields.values())
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

        elif '{value_as_tuple}' in where_text:
            value = Utils.format_as_sql_values_tuple(value)
            return where_text.format(
                column=column,
                value_as_tuple=value
            )

        return where_text.format(
            column=column,
            value=Utils.convert_to_sql_type(value)
        )
        
