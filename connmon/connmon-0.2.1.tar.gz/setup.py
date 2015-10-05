from setuptools import setup
from setuptools import find_packages
import os
import re


with open(
    os.path.join(os.path.dirname(__file__), 'connmon', '__init__.py')
) as file_:
    VERSION = re.compile(
        r".*__version__ = '(.*?)'", re.S).match(file_.read()).group(1)


readme = os.path.join(os.path.dirname(__file__), 'README.rst')

requires = [
    'SQLAlchemy>=1.0.5',
    'eventlet',
    'zkcluster>=0.0.2'
]

setup(
    name='connmon',
    version=VERSION,
    description="Analyze database connection usage",
    long_description=open(readme).read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Database :: Front-Ends',
    ],
    keywords='SQLAlchemy',
    author='Mike Bayer',
    author_email='mike@zzzcomputing.com',
    url='http://bitbucket.org/zzzeek/connmon',
    license='MIT',
    packages=find_packages('.', exclude=['examples*', 'test*']),
    include_package_data=True,
    tests_require=['mock'],
    zip_safe=False,
    install_requires=requires,
    entry_points={
        'console_scripts': [
            'connmon = connmon.frontend:monitor',
            'connmond = connmon.frontend:connmond',
        ],
        'sqlalchemy.dialects': [
            'mysql.connmon = connmon.plugin:CMWrapper',
            'mysql.mysqldb_connmon = connmon.plugin:CMWrapper',
            'mysql.pymysql_connmon = connmon.plugin:CMWrapper',
            'sqlite.connmon = connmon.plugin:CMWrapper',
            'postgresql.connmon = connmon.plugin:CMWrapper',
            'postgresql.psycopg2_connmon = connmon.plugin:CMWrapper',
        ]
    }
)
