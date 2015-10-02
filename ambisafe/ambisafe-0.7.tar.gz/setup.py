import os
from setuptools import setup, find_packages

VERSION = '0.7'

BASEDIR = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(BASEDIR, 'README.rst')).read()

setup(
    name='ambisafe',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests >= 2.7.0",
        "pyOpenSSL >= 0.15.1",
        "ecdsa >= 0.13",
        "pycrypto >= 2.6.1",
        "pybitcointools == 1.1.15"
    ],
    url='https://bitbucket.org/ambisafe/client-python',
    download_url='https://bitbucket.org/ambisafe/client-python/get/{0}.zip'
        .format(VERSION),
    author='Anton Simernia',
    author_email='anton.simernia@ambisafe.co',
    keywords=['ambisafe', 'bitcoin'],
    description='Ambisafe server client library',
    long_description=README,
    classifiers=[
        'Intended Audience :: Developers',
    ],
    test_suite='test.test',
    setup_requires=[
        "flake8",
        "nose>=1.0",
        "coverage",
        "mock"
    ]
)
