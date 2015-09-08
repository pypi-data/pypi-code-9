import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name = "processcall",
        version = "1.1.0",
        author = "ruifengyun",
        author_email = "rfyiamcool@163.com",
        description = "a simple subprocess manager,suport stream stdout \ async ",
        packages=['processcall'],
        license = "MIT",
        keywords = ["subprocess processcall","fengyun"],
        url = "https://github.com/rfyiamcool/simpleprocess",
        long_description = read('README.md'),
        classifiers = [
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.0',
        'Topic :: Software Development :: Libraries :: Python Modules',
            ]
        )

