from setuptools import setup

setup(
    name='ksr',
    version='0.1',
    py_modules=['ksr'],
    install_requires=[
        'Click',
        'TinyDB',
    ],
    entry_points='''
        [console_scripts]
        ksr=ksr:cli
    ''',
)
