# tiny_sqlite_orm

A simple ORM (Object-Relational Mapping) library for interacting with SQLite databases in Python, allowing you to work with your data in an object-oriented manner. The library focuses on simplicity and ease of use for small projects.

## Installation

You can install it by running:

```bash
pip install tiny_sqlite_orm
```

## How to use

### Setting up the database connection

First, you need to create an instance of the `Database` class to connect to the SQLite database.

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

### Creating the tables

After defining your models, you can create the tables in the database:

```python
# Create the tables if they don't already exist
db.create_tables_if_not_exists([User])
```

### Inserting data

You can insert new records into the database by running:

```python
# Create a new user
user = User.create(name="John", age=30)
user.name
# Returns: John
```

### Selecting data

To query data from the database, you can use the `select` method:

```python
# Fetch users with age greater or
# equal (__ge) than 15
users = User.objects.select(
    age__ge=15
)

# Iterate over the results
for user in users:
    print(user.name, user.age)

users.first()
users.last()
```

### Updating records

To update a record, you can:

- modify the object's attributes and call the `save` method again:

```python
user = User.objects.select(name="John").first()
if user:
    user.age = 31
    user.save()
```

- use the `Table.objects.update()` method:

```python
User.objects.update(
    # Updates the age to 31
    fields={'age': 31},
    # Where name is "John"
    name="Jonh"
)
```

### Deleting records

You can delete a record by calling the `delete` method on the object:

```python
# Delete a user
user = User.objects.select(name="John").first()
if user:
    user.delete()
```

Or using the delete method:

```python
# Delete all users with
# name John
User.objects.delete(name="John")
```

### Using ForeignKey

You can also define foreign key relationships between models. Here's an example with a `Post` model referencing a `User`:

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

### Aggregations Support

The library supports aggregation operations such as `count`, `sum`, `avg`, `max`, and `min`:

```python
# Count the number of users
total_users = User.objects.count()

# Get the average age of users
average_age = User.objects.avg('age')

print(f'Total users: {total_users}')
print(f'Average age: {average_age}')
```

## Contributions

Contributions are welcome! Feel free to open a PR or suggest improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.