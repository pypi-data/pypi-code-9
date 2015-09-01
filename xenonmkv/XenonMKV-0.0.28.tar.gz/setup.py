# coding=utf8
import os
import re
from setuptools import setup

def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as f:
        return f.read()


def get_version(filename='xenonmkv/__init__.py'):
    for line in read(filename).splitlines():
        if line.startswith('__version__'):
            d = {}
            exec(line, d)
            return d['__version__']
    raise AssertionError("couldn't find __version__ in %s" % filename)


version = get_version()

setup(
    name='XenonMKV',
    version=version,
    author=u'barisariburnu',
    author_email='barisariburnu@gmail.com',
    keywords='MKV Container MP4 XenonMKV',
    url='https://github.com/barisariburnu/xenonmkv',
    download_url='https://github.com/barisariburnu/xenonmkv/tarball/' + version,
    packages=['xenonmkv', 'xenonmkv.utils'],
    include_package_data=True,
    install_requires=[],
    description='XenonMKV is a video container conversion tool that takes MKV files and outputs them as MP4 files.',
    long_description=read('README.rst'),
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'xenonmkv = xenonmkv.xenonmkv:main',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Utilities',
    ],
)
