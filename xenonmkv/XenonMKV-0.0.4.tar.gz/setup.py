# coding=utf8
import os
import re
from setuptools import setup


def read(*fname):
    with open(os.path.join(os.path.dirname(__file__), *fname)) as f:
        return f.read()


def get_version():
    for line in read('xenonmkv', '__init__.py').splitlines():
        m = re.match(r"""__version__\s*=\s*['"](.*)['"]""", line)
        if m:
            return m.groups()[0].strip()
    raise Exception('Cannot find version')


setup(
    name='XenonMKV',
    version=get_version(),
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
    long_description=read('README.md'),
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
