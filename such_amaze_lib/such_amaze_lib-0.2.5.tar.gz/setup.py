from setuptools import setup, find_packages

version = '0.2.5'
author = 'Blaise Fulpin'

setup(
    name='such_amaze_lib',
    version=version,
    packages=find_packages(),
    author=author,
    author_email='blaise.fulpin@gmail.com',
    description='Such Amaze Library, Much Wow Functions',
    long_description=open('README.rst').read(),
    include_package_data=True,
    url='https://bitbucket.org/BlaiseFulpin/such_amaze_lib',
    classifiers=[
        "Programming Language :: Python",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
    ]
)
