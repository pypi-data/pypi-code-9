import codecs
from setuptools import find_packages, setup

setup(
    name='json-awk',
    version='1.0.1.dev1',
    license='GPLv2',
    author='Pierre-Gildas MILLON',
    author_email='pg.millon@gmail.com',
    description='A simple JSON parser and printer',
    long_description=codecs.open('README.rst', encoding='utf-8').read(),
    url='https://github.com/pgmillon/json-awk',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='json awk',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    ]
)
