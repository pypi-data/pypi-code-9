from setuptools import setup
import os

setup(
    name="tipy",
    version="0.3.3",
    author="Mathieu Fourcroy",
    author_email="mathieu.fourcroy@gmail.com",
    packages=["tipy"],
    package_dir={'tipy': 'tipy'},
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing :: Linguistic',
    ],
    keywords='text prediction competer keyboard',
    include_package_data=True,
    url="http://pypi.python.org/pypi/tipy/",
    license="GPL",
    description="Text predictor.",
    long_description=open("README.txt").read(),
    data_files=[
        (os.path.join(os.path.expanduser("~"), '.config/tipy'),
            ['cfg/tipy.ini']),
        (os.path.join(os.path.expanduser("~"), '.config/tipy/databases'), 
            ['databases/corp.db',
             'databases/dict.db',
             'databases/fb.db',
             'databases/user.db'
             ]),
        (os.path.join(os.path.expanduser("~"), '.config/tipy/dicttionaries'), 
            ['dictionaries/en_US.dic']),
        (os.path.join(os.path.expanduser("~"), '.config/tipy/stoplists'), 
            ['stoplists/insanities_en.stoplist']),
        (os.path.join(os.path.expanduser("~"), '.config/tipy/txt'), 
            ['txt/brown.txt',
             'txt/fb.txt',
             'txt/fr.txt'
            ]),
        ('/usr/share/tipy',
            ['cfg/tipy.ini']),
        ('/usr/share/tipy/databases', 
            ['databases/corp.db',
             'databases/dict.db',
             'databases/fb.db',
             'databases/user.db'
             ]),
        ('/usr/share/tipy/dicttionaries', 
            ['dictionaries/en_US.dic']),
        ('/usr/share/tipy/stoplists', 
            ['stoplists/insanities_en.stoplist']),
        ('/usr/share/tipy/txt', 
            ['txt/brown.txt',
             'txt/fb.txt',
             'txt/fr.txt'
            ]),
    ],
    entry_points = {"console_scripts": ['tipy=tipy.main:main']},
    install_requires=["requests",],
)
