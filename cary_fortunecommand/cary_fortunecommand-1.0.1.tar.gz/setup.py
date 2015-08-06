from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

long_description = """
A simple Cary command which runs the cowsay and fortune commands and
replies with the fortune
"""

setup(
    name='cary_fortunecommand',
    version='1.0.1',
    url='https://github.com/vputz/cary',
    description='cary command for the unix cowsay and fortune commands',
    long_description=long_description,
    author='Victor Putz',
    author_email='vputz@nyx.net',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Email',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        ],

    keywords='email',

    packages=['cary_fortunecommand'],

    install_requires=['cary'],

    extras_require={},

)
