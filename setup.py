from setuptools import setup, find_packages


setup(
    name="so2sql",
    version="0.1",
    packages=find_packages(),
    install_requires=[
            "sqlalchemy",
            "stackapi"
            "bs4",
    ],
    test_suite="tests"
)
