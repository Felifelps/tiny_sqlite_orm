from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="tiny_sqlite_orm",
    version="1.2.0",
    author="Felifelps",
    author_email="felifelps.dev@gmail.com",
    description="A simple ORM for SQLite databases in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Felifelps/tiny_sqlite_orm",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
