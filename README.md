# tiny_sqlite_orm

A simple ORM (Object-Relational Mapping) library for interacting with SQLite databases in Python, allowing you to work with your data in an object-oriented manner. The library focuses on simplicity and ease of use for small projects.

## Installation

You can install it by running:

```bash
pip install tiny_sqlite_orm
```

## How to Use

### Setting Up the Database Connection

First, create an instance of the `Database` class to connect to the SQLite database.

```python
from sqlite_orm.database import Database

# Connect to the database (or create it if it doesn't exist)
db = Database('my_database.db')
```

### Defining Models

Models are defined as subclasses of the `Table` class. Each field in the model is an instance of a `Field` class. Here's an example of how to create a simple model:

```python
from sqlite_orm.table import Table
from sqlite_orm.field import TextField, IntegerField

class User(Table):
    # Bind the database to the model within the class
    db = db

    # Table fields
    name = TextField(unique=True)
    age = IntegerField()
```

### Creating the Tables

After defining your models, you can create the tables in the database:

```python
# Create the tables if they don't already exist
db.create_tables_if_not_exists([User])
```

### Inserting Data

You can insert new records into the database by running:

```python
# Create a new user
user = User.create(name="John", age=30)
print(user.name)  # Returns: John
```

### Selecting Data

To query data from the database, you can use the `select` method:

```python
# Fetch users with age greater than or equal to 15
users = User.objects.select(age__ge=15)

# Iterate over the results
for user in users:
    print(user.name, user.age)

# Access the first and last user
first_user = users.first()
last_user = users.last()
```

See more about using [select filters.](#using-select-filters)

### Updating Records

To update a record, you can:

- Modify the object's attributes and call the `save` method:

```python
user = User.objects.select(name="John").first()
if user:
    user.age = 31
    user.save()
```

- Use the `Table.objects.update()` method:

```python
User.objects.update(
    # Updates the age to 31
    fields={'age': 31},
    # Where name is "John"
    name="John"
)
```

### Deleting Records

You can delete a record by calling the `delete` method on the object:

```python
# Delete a user
user = User.objects.select(name="John").first()
if user:
    user.delete()
```

Or you can delete records using the delete method:

```python
# Delete all users with the name John
User.objects.delete(name="John")
```

### Using ForeignKey

You can define foreign key relationships between models. Here's an example with a `Post` model referencing a `User`:

```python
from sqlite_orm.field import ForeignKeyField

class Post(Table):
    # Bind the database within the class
    db = db
    title = TextField()
    author = ForeignKeyField(User)

# Create the Post table
db.create_tables_if_not_exists([Post])

# Create a post related to a user
Post.create(title="My first post", author=user)
```

### Aggregation Support

The library supports aggregation operations such as `count`, `sum`, `avg`, `max`, and `min`:

```python
# Count the number of users
total_users = User.objects.count()

# Get the average age of users
average_age = User.objects.avg('age')

print(f'Total users: {total_users}')
print(f'Average age: {average_age}')
```

### Using Select Filters

This method supports a variety of filters using `__` (double underscore) syntax to specify conditions. Here are some common operators you can use:

- `No filters`: Checks for equality (e.g., `field=value`).
- `field__ne`: Checks for inequality (e.g., `field__ne=value`).
- `field__gt`: Checks if the field is greater than a value (e.g., `field__gt=value`).
- `field__ge`: Checks if the field is greater than or equal to a value (e.g., `field__ge=value`).
- `field__lt`: Checks if the field is less than a value (e.g., `field__lt=value`).
- `field__le`: Checks if the field is less than or equal to a value (e.g., `field__le=value`).
- `field__in`: Checks if the field is in one of the values passed (e.g., `field__in=[1, 2, 'test']`).

The two below only work for string fields:
- `field__contains`: Checks if the field's value contains the value (case sensitive) (e.g., `field__contains="a"`).
- `field__icontains`: Also checks if the field's value contains the value, but is case insensitive.

Here’s an example of how to use these operators in a query:

```python
# Fetch users with age greater than or equal to 15
users = User.objects.select(age__ge=15)

# Fetch users whose name starts with exactly 'Jo'
users_with_Jo = User.objects.select(name__contains='Jo')

# Fetch users whose age is either 25 or 30
users_25_or_30 = User.objects.select(age__in=[25, 30])

# Iterate over the results
for user in users:
    print(user.name, user.age)

# Access the first and last user
first_user = users.first()
last_user = users.last()
```

## Contributions

Contributions are welcome! Feel free to open a pull request or suggest improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.