try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from pip.req import parse_requirements
from pip.download import PipSession

setup(
    description='freeze arbitrary Python things as immutables',
    author='Andrew Pennebaker',
    url='https://github.com/mcandre/liquidnitrogen',
    download_url='git@github.com:mcandre/liquidnitrogen.git',
    author_email='andrew.pennebaker@gmail.com',
    version='0.0.0',
    install_requires=[
        str(r.req)
        for r in parse_requirements('requirements.txt', session=PipSession())
    ],
    packages=['liquidnitrogen'],
    package_data={'': ['requirements.txt']},
    include_package_data=True,
    scripts=[],
    name='liquidnitrogen',
    license='FreeBSD'
)
