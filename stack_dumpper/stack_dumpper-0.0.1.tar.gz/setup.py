from setuptools import setup

setup(
    name='stack_dumpper',
    version='0.0.1',
    author='Jayson Reis',
    author_email='santosdosreis@gmail.com',
    description='Dump stack trace from all threads (including main thread) when CRTL + \ is pressed or SIGQUIT is received.',
    url='https://github.com/jaysonsantos/python-stack-dumpper',
    packages=['stack_dumpper'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
    ]
)
