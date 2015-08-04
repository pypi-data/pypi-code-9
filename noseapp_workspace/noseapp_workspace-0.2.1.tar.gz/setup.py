# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages


__version__ = '0.2.1'


if __name__ == '__main__':
    setup(
        name='noseapp_workspace',
        url='https://github.com/trifonovmixail/noseapp_workspace',
        version=__version__,
        packages=find_packages(),
        author='Mikhail Trifonov',
        author_email='mikhail.trifonov@corp.mail.ru',
        description='workspace extension for noseapp lib',
        long_description=open('README.rst').read(),
        include_package_data=True,
        zip_safe=False,
        platforms='any',
        install_requires=[
            'noseapp>=1.0.9',
        ],
        test_suite='tests',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Topic :: Software Development :: Testing',
        ],
    )
