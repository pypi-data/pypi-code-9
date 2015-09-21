import setuptools

setuptools.setup(
    name="Flask-CassandraDB",
    version="0.0.1",
    url="https://github.com/youngking/flask-cassandradb",

    author="Young King",
    author_email="yanckin@gmail.com",

    description="connect cassandra to flask",
    long_description=open('README.rst').read(),
    packages=setuptools.find_packages(),
    py_modules=['flask_cassandradb'],
    install_requires=[
        'Flask',
        'cassandra-driver'
    ],


    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
)
