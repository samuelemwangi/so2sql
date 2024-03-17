from setuptools import setup, find_packages

VERSION = "0.0.13"
DESCRIPTION = "Library to fetch StackOverflow data and persist it to an SQL database"
LONG_DESCRIPTION = """
Helps to fetch StackOverflow data and persist it to an SQL database. 
Makes use of StackAPI and SQLAlchemy.
"""

setup(
    name="so2sql",
    version=VERSION,
    author="samuelemwangi",
    url="https://github.com/samuelemwangi/so2sql",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
            "SQLAlchemy",
            "StackAPI",
            "beautifulsoup4",
            "numpy",
            "pandas"
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    test_suite="tests"
)
