# Changelog

All notable changes to this library will be documented in this file.

## [1.2.0] - 2024-10-07

### Added
- Implemented new field types:
  - `CharField` with `max_length` validation.
  - `DateField` with `auto_today` functionality for default date values.
  - `DatetimeField` with `auto_now` functionality for default datetime values.
  - `BooleanField` for true/false values.
  - `ForeignKeyField` for creating relationships between models.
- Introduced filters for `objects.select` queries:
  - Support for comparison operators: `__ne`, `__gt`, `__ge`, `__lt`, `__le`.
  - Support for `__in` operator for matching multiple values.
  - String field search filters: `__contains` (case-sensitive) and `__icontains` (case-insensitive).
- Added support for aggregation functions in `Queryset`:
  - `count`, `sum`, `avg`, `min`, `max`.

### Changed
- Improved schema generation logic for tables, including handling of primary keys (`AutoField`) and foreign keys.
- Refined error handling and messages for invalid field types and data insertion issues.
- Enhanced validation mechanisms for fields:
  - Ensured `CharField` checks for max length.
  - Added validation for date and datetime format in `DateField` and `DatetimeField`.
  
### Fixed
- Addressed issues with string representation of SQL queries in `Queryset`.
- Fixed bugs related to table creation with complex field definitions and foreign key relationships.
