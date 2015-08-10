"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages

setup(
    name='twitchwatcher',

    version='0.0.1',

    description='A tiny wrapper for livestreamer to watch twitch streams',
    long_description='A tiny wrapper to launch livestreamer made specificly for twitch streams',

    url='https://github.com/MOZGIII/twitchwatcher',

    author='MOZGIII',
    author_email='mike-n@narod.ru',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: End Users/Desktop',
        'Topic :: Games/Entertainment',
        'Topic :: Internet',
        'Topic :: Multimedia :: Video :: Display',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],

    keywords='twitch livestreamer stream twitch.tv',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=['livestreamer'],

    entry_points={
        'console_scripts': [
            'twitchwatcher=twitchwatcher:main',
            'twitch=twitchwatcher:main',
        ],
    },
)
