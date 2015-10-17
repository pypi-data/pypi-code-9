import sys
from setuptools import setup
import zones

setup(
    name='krebszones',
    version=zones.__version__,

    description='Manages DNS Zones via differnt APIs',
    long_description=open("README.md").read(),
    license='WTFPL',
    url='http://krebsco.de/',
    download_url='https://pypi.python.org/pypi/krebs-zones/',

    author='makefu',
    author_email='spam@krebsco.de',
    install_requires = [ 'docopt','ovh' ],

    packages=['zones'],
    entry_points={
        'console_scripts' : [
            'ovh-zone = zones.ovhzone:main'
            ]
        },

    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)

