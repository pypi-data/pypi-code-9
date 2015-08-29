from setuptools import setup
from pip.req import parse_requirements
import io
import os
import int_date

__author__ = 'Cedric Zhuang'


def here(filename=None):
    ret = os.path.abspath(os.path.dirname(__file__))
    if filename is not None:
        ret = os.path.join(ret, filename)
    return ret


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n\n')
    buf = []
    for filename in filenames:
        with io.open(here(filename), encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


requirements = parse_requirements('requirements.txt', session=False)


def get_long_description():
    filename = 'README.md'
    try:
        import pypandoc
        ret = pypandoc.convert(filename, 'rst')
    except ImportError:
        ret = read(filename)
    return ret


setup(
    name="int_date",
    version=int_date.__version__,
    author="Cedric Zhuang",
    author_email="cedric.zhuang@gmail.com",
    description="Utility for int date like 20150312.",
    license="BSD",
    keywords="date integer",
    url="http://github.com/jealous/int_date",
    packages=['int_date'],
    platforms=['any'],
    long_description=get_long_description(),
    classifiers=[
        "Programming Language :: Python",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    install_requires=[str(ir.req) for ir in requirements],
    tests_require=['pytest', 'pyhamcrest']
)
