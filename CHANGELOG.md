# Changelog

All notable changes to this library will be documented in this file.

## [1.1.0] - 2024-10-05
### Added
- New filters for the `objects.select` statement, including support for `__ne`, `__gt`, `__ge`, `__lt`, `__le`, and `__in` operators.
- String field search options, including `__contains` and `__icontains`.
- Updated documentation to include examples of new filters.

### Changed
- Restructured code for better clarity.
- Improved error messages for database operations.

## [1.0.0] - 2024-09-25
### Added
- Initial creation of the `tiny_sqlite_orm` library for interacting with SQLite databases in Python.
- Basic functionalities such as model creation, data insertion and selection, updates, and deletions.
- Support for foreign key relationships between models.
- Aggregation functionality with methods like `count`, `avg`, `sum`, `min`, and `max`.

## [0.1.0] - 2024-09-20
### Added
- Initial structure of the library.
- Functionality to connect to an SQLite database.
- Basic model for data manipulation.
