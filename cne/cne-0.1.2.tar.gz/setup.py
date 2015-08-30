import os

from setuptools import setup


def readme(*paths):
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
    name='cne',
    version='0.1.2',
    description='Get fuel price from cne api',
    long_description=readme('README.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='cne fuel api',
    url='http://github.com/lgaticaq/python-cne',
    author='Leonardo Gatica',
    author_email='lgatica@protonmail.com',
    license='MIT',
    packages=['cne'],
    py_modules=['cne'],
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False)
