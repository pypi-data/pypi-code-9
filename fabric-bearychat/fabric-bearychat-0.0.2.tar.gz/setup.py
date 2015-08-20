# coding: utf-8

from setuptools import setup


version = '0.0.2'

desc = 'Fabric task aided with bearychat.'

install_requires = [
    'fabric>=1.7.0',
    'bearychat-py>=0.3.1',
]


setup(
    name='fabric-bearychat',
    version=version,
    author='hbc',
    author_email='bcxxxxxx@gmail.com',
    url='https://github.com/bcho/fabric-bearychat',
    description=desc,
    license='MIT',
    py_modules=['fabric_bearychat'],
    install_requires=install_requires,
    zip_safe=False,
    include_package_data=True,

    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
        'Programming Language :: Python :: 2.7',
    ]
)
