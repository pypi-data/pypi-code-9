# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from thugperf import __version__

setup(
    name='thugperf',
    version=__version__,
    description="simple page load time measurement tool",
    long_description="simple page load time measurement tool",
    keywords='web load time measurement tool',
    author='Guilherme Souza',
    author_email='guivideojob@gmail.com',
    license='MIT',
    url='https://github.com/guilhermef/thugperf',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(),
    package_dir={"thugperf": "thugperf"},
    include_package_data=True,

    install_requires=[
        'seleniumwrapper',
        'xvfbwrapper'
    ],

    entry_points={
        'console_scripts': [
            'thugperf=thugperf.runner:main',
        ],
    },

)
