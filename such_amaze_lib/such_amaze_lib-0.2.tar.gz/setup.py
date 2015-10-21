from setuptools import setup, find_packages

import setup_cfg

setup(
    name='such_amaze_lib',
    version=setup_cfg.__version__,
    packages=find_packages(),
    author=setup_cfg.__author__,
    author_email='blaise.fulpin@gmail.com',
    description='Such Amaze Library, Much Wow Functions',
    long_description=open('README.md').read(),
    include_package_data=True,
    url='https://bitbucket.org/BlaiseFulpin/such_amaze_lib',
    classifiers=[
        "Programming Language :: Python",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
    ]
)
