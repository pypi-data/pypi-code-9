#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from setuptools import setup,find_packages

setup(
    name='ucloudclient',
    version='0.2.2',
    # packages=['ucloudclient'],
    packages = find_packages(),
    # package_dir = {'':'ucloudclient'},
    keywords=('ucloud', 'client'),
    description='Ucloud(Ucloud.cn) python client and command line tools.'
                'Author\'s bolg http://yanheven.github.io',
    license='Apache License Version 2.0',
    url='https://github.com/yanheven/ucloud-python-sdk',
    author='yanhaifeng(颜海峰)',
    author_email='yanheven@gmail.com',

    include_package_data=True,
    platforms='any',
    install_requires=['PrettyTable>=0.7,<0.8', 'six>=1.9.0'],
    entry_points={
        'console_scripts': ['ucloud=ucloudclient.shell:main'],
    }
)
