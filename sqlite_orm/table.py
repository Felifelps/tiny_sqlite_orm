from .field import Field, AutoField
from .queryset import Queryset
from .database import Database


class Table:

    db = None

    @classmethod
    def create(cls, **kwargs) -> None:
        return cls.objects.insert(**kwargs)

    def __init_subclass__(cls):
        cls.__check_if_db_is_defined()
        cls.__initialize()

    @classmethod
    def __check_if_db_is_defined(cls):
        if not isinstance(cls.db, Database):
            raise AttributeError('Set "Table.db" attribute to a "Database" object when inherit from "Table" class')

    @classmethod
    def __initialize(cls):
        cls.__set_attributes()
        cls.__set_fields_name()
        cls.__handle_primary_key()
        cls.__mount_schema()

    @classmethod
    def __set_attributes(cls):
        cls.table_name = cls.__name__.lower()
        cls.objects = Queryset(cls)
        cls.pk = None

    @classmethod
    def __set_fields_name(cls):
        for attr_name, attr in cls.__dict__.items():
            if cls.__is_field(attr):
                attr._name = attr_name

    @classmethod
    def __is_field(cls, attr):
        return isinstance(attr, Field)

    @classmethod
    def __handle_primary_key(cls):
        for field in cls.get_fields():
            if field.primary_key:
                return cls.__set_pk(field)

        cls.__create_id_and_set_as_pk()

    @classmethod
    def get_fields(cls):
        for attr_name, attr in cls.__dict__.items():
            if cls.__is_field(attr) and attr_name != 'pk':
                yield attr

    @classmethod
    def __create_id_and_set_as_pk(cls):
        cls.id = AutoField(
            primary_key=True,
            _name='id'
        )
        cls.__set_pk(cls.id)

    @classmethod
    def __set_pk(cls, pk):
        cls.pk = pk

    @classmethod
    def __mount_schema(cls):
        columns_schema = cls.__get_columns_schema()

        cls._schema = (
            f'CREATE TABLE IF NOT EXISTS {cls.table_name} '
            f'({columns_schema});'
        )

    @classmethod
    def __get_columns_schema(cls):
        fields_schema = ', '.join(field._schema for field in cls.get_fields())
        foreign_keys_schema = ', '.join(
            field.foreign_key_schema for field in cls.get_fields() if hasattr(field, 'foreign_key_schema')
        )
        columns_schema = [fields_schema]
        if foreign_keys_schema:
            columns_schema.append(foreign_keys_schema)

        return ', '.join((
            columns_schema
        ))
