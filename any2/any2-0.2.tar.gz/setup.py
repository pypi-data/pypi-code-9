# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

version = '0.2'

setup(
    name='any2',
    version=version,
    description="Base package for any2*",
    long_description="""\
""",
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[],
    keywords='',
    author='Florent Aide',
    author_email='florent.aide@gmail.com',
    url='https://bitbucket.org/faide/any2',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "six",
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
