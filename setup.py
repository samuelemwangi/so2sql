from setuptools import setup, find_packages

VERSION = "0.0.1"
DESCRIPTION = "Library to fetch StackOverflow data and persist it to an SQL database"
LONG_DESCRIPTION = open("README.md").read()

setup(
    name="so2sql",
    version=VERSION,
    author="samuelemwangi",
    author_email="sammiemwangi4@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
            "sqlalchemy",
            "stackapi"
            "bs4",
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
