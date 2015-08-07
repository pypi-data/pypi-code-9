from setuptools import setup

version = '0.0.1'
name = 'vgmdb_wrapper'
short_description = 'VGMdb API Wrapper for Python.'
long_description = """
VGMdb API Wrapper for Python
"""

classifiers = [
   "Development Status :: 1 - Planning",
   "License :: OSI Approved :: MIT License",
   "Programming Language :: Python :: 2 :: Only",
   "Topic :: Software Development",
]

setup(
    name=name,
    version=version,
    description=short_description,
    long_description=long_description,
    classifiers=classifiers,
    keywords=['vgmdb',],
    author='Kanatani Kazuya',
    author_email='kanatani.devel@gmail.com',
    url='https://github.com/kinformation/vgmdb_wrapper',
    license='MIT License',
)
