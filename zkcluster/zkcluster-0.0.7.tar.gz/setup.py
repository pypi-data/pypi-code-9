from setuptools import setup
from setuptools import find_packages
import os
import re


with open(
        os.path.join(
            os.path.dirname(__file__),
            'zkcluster', '__init__.py')) as v_file:
    VERSION = re.compile(
        r".*__version__ = '(.*?)'",
        re.S).match(v_file.read()).group(1)

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as r_file:
    readme = r_file.read()


requires = [
    'eventlet'
]

setup(
    name='zkcluster',
    version=VERSION,
    description="zzzeek's clustering server framework",
    long_description=readme,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    author='Mike Bayer',
    author_email='mike@zzzcomputing.com',
    url='http://bitbucket.org/zzzeek/zkcluster',
    license='MIT',
    packages=find_packages('.', exclude=['test*']),
    include_package_data=True,
    tests_require=['mock'],
    zip_safe=False,
    install_requires=requires,
    entry_points={
    }
)
