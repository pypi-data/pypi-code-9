# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

version = '0.1'

setup(
    name='any2xl',
    version=version,
    description="A library to generate Excel files from Python iterables",
    long_description="""\
""",
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial :: Spreadsheet",
    ],
    keywords='xls xlsx adapter',
    author='Florent Aide',
    author_email='florent.aide@gmail.com',
    url='https://bitbucket.org/faide/any2xl',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "six",
        "any2 >= 0.3",
        "openpyxl",
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
