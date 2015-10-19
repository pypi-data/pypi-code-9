# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='tc_aws',
    version='2.0.7',
    description='Thumbor AWS extensions',
    author='Thumbor-Community & William King',
    author_email='willtrking@gmail.com',
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    install_requires=[
        'python-dateutil',
        'thumbor>=5.2',
        'tornado-botocore',
    ],
    extras_require={
        'tests': [
            'pyvows',
            'coverage',
            'tornado_pyvows',
            'boto',
            'moto',
            'mock',
        ],
    },
)
