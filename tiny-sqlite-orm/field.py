from datetime import date, datetime
from .record import Record
from .utils import Utils


class Field:

    default = None
    primary_key = False
    null = False
    unique = False

    _name = None
    _python_type = None
    _type = ''

    __schema = None

    def __init__(self, **options):
        self.__setup_options(options)

    def __setup_options(self, options):
        self._check_if_is_wrong_type(options.get('default'))

        for option, value in options.items():
            setattr(self, option, value)

    def _check_field_value(self, value):
        self._check_if_can_be_none(value)
        self._check_if_is_wrong_type(value)

    def _check_if_can_be_none(self, value):
        if value is None and not self.null:
            raise ValueError(f'Field "{self._name}" cannot be "None"')

    def _check_if_is_wrong_type(self, value):
        try:
            value = self._python_type(value)
        except (ValueError, TypeError):
            pass
        if value is not None and not isinstance(value, self._python_type): 
            raise ValueError(
                f'The "{self._name}" field expected {self._python_type}", not "{type(value)}"'
            )

    @property
    def _schema(self):
        self.__check_if_name_is_defined()
        if not self.__schema:
            self._mount_schema()
        return self.__schema

    def __check_if_name_is_defined(self):
        if self._name is None:
            raise AttributeError('Set "Field._name" attribute before getting Field._schema')

    def _mount_schema(self):
        schema = f'{self._name} {self._type}'

        if self.null:
            schema += ' NULL'

        if self.unique:
            schema += ' UNIQUE'

        if self.primary_key:
            schema += ' PRIMARY KEY'

        default = self.default
        if default is not None:
            default = Utils.convert_to_sql_type(default)
            schema += f' DEFAULT {default}'

        self.__schema = schema

    def _convert_sql_value_to_python(self, value):
        return self._python_type(value)

class IntegerField(Field):

    _python_type = int
    _type = 'INTEGER'


class AutoField(IntegerField):

    def _mount_schema(self):
        super()._mount_schema()
        self._Field__schema += ' AUTOINCREMENT'

class FloatField(Field):

    _python_type = float
    _type = 'REAL'


class BooleanField(Field):

    _python_type = bool
    _type = 'BOOLEAN'


class TextField(Field):

    _python_type = str
    _type = 'TEXT'


class CharField(Field):

    _python_type = str
    _type = 'VARCHAR'

    def __init__(self, max_length, **kwargs: dict):
        super().__init__(max_length=max_length, **kwargs)

    def _mount_schema(self):
        self._type = f"{self._type}({self.max_length})"
        super()._mount_schema()
        self._type = 'VARCHAR'


class DateField(TextField):

    def __init__(self, auto_today=False, **options):
        if auto_today:
            options['default'] = date.today()
        super().__init__(**options)

    def _check_if_is_wrong_type(self, value):
        if isinstance(value, date):
            value = value.isoformat()
        elif isinstance(value, str):
            self.__matches_isoformat(value)
        return super()._check_if_is_wrong_type(value)

    def __matches_isoformat(self, value):
        try:
            date.fromisoformat(value)
        except ValueError:
            raise ValueError(
                f'String "{value}" does not match '
                f'isoformat "YYYY-MM-DD"'
            )

    def _convert_sql_value_to_python(self, value):
        if isinstance(value, str):
            return date.fromisoformat(value)
        return value


class DatetimeField(TextField):

    def __init__(self, auto_now=False, **options):
        if auto_now:
            options['default'] = datetime.now()
        super().__init__(**options)

    def _check_if_is_wrong_type(self, value):
        if isinstance(value, datetime):
            value = value.isoformat()
        elif isinstance(value, str):
            self.__matches_isoformat(value)
        return super()._check_if_is_wrong_type(value)

    def __matches_isoformat(self, value):
        try:
            datetime.fromisoformat(value)
        except ValueError:
            raise ValueError(
                f'String "{value}" does not match '
                f'isoformat "YYYY-MM-DD HH:MM:SS"'
            )

    def _convert_sql_value_to_python(self, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value


class ForeignKeyField(Field):

    def __init__(self, ref_table, on_delete=False):
        self.ref_table = ref_table
        self._type = self.ref_table.pk._type
        self._python_type = self.ref_table.pk._python_type
        super().__init__(
            on_delete=on_delete
        )

    def _mount_schema(self):
        self.__set_foreign_key_schema()

        schema = self.ref_table.pk._schema

        schema = schema.replace('PRIMARY KEY', '')
        schema = schema.replace('AUTOINCREMENT', '')

        schema_words = schema.split(' ')
        schema_words[0] = self._name

        self._Field__schema = ' '.join(schema_words)

    def __set_foreign_key_schema(self):
        self.foreign_key_schema = (
            f'FOREIGN KEY ({self._name}) '
            f'REFERENCES {self.ref_table.table_name}'
            f'({self.ref_table.pk._name})'
        )

    def _check_if_is_wrong_type(self, field):
        if isinstance(field, Record):
            field = field.pk
        return super()._check_if_is_wrong_type(field)

    def _convert_sql_value_to_python(self, value):
        args = {self.ref_table.pk._name: value}
        return self.ref_table.objects.select(**args).first()
