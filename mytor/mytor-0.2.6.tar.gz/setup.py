# encoding: utf-8
from setuptools import setup

setup(
    name='mytor',
    version='0.2.6',
    packages=['mytor'],
    install_requires=[
        'tornado>=4.1',
        'PyMySQL==0.6.7',
        'greenlet>=0.4.2',
    ],
    author=['snower', 'mosquito'],
    author_email=['sujian199@gmail.com', 'me@mosquito.su'],
    url='https://github.com/mosquito/mytor',
    license='MIT',
    keywords=[
        "tornado", "mysql"
    ],
    description='Tornado asynchronous MySQL Driver [fork of TorMysql]',
    long_description=open("README.rst").read(),
    zip_safe=False,
)
