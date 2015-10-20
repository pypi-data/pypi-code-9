# coding=utf8

from setuptools import setup, find_packages
__author__ = 'hellflame'


setup(
    name='FlowCheck',
    version='0.4',
    keywords=('quantity of flow', 'flow check', 'flow'),
    description="在linux终端基于ip命令获取统计通过网卡的流量信息",
    license='MIT',
    author="hellflame",
    author_email="hellflamedly@gmail.com",
    url='https://github.com/hellflame/flow_check',
    packages=find_packages(),
    platforms='Ubuntu',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7"
    ],
    entry_points={
        'console_scripts': [
            'flower=flow.flower:main'
        ]
    }
)

