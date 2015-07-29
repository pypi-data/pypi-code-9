# coding=utf8
import os
import re
from setuptools import setup

setup(
    name='XenonMKV',
    version='0.0.5',
    author=u'barisariburnu',
    author_email='barisariburnu@gmail.com',
    keywords='MKV Container MP4 XenonMKV',
    url='https://github.com/barisariburnu/xenonmkv',
    download_url = 'https://github.com/barisariburnu/xenonmkv/tarball/0.0.4',
    packages=['xenonmkv'],
    include_package_data=True,
    install_requires=[
        'mediainfo>=0.7.60',
        'mkvtoolnix>=5.7.0',
        'mplayer>=0.7.0',
        'faac>=1.28',
        'gpac>=0.5.0',
    ],
    description='XenonMKV is a video container conversion tool that takes MKV files and outputs them as MP4 files.',
    long_description=open('README.md').read(),
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'xenonmkv = xenonmkv:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Utilities',
    ],
)
