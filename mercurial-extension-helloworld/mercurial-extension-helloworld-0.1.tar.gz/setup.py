import os
from setuptools import setup, find_packages

current_dir = os.path.dirname(os.path.abspath(__file__))


def read(filename):
    fullpath = os.path.join(current_dir, filename)
    try:
        with open(fullpath) as f:
            return f.read()
    except Exception:
        return ""


setup(
    name='mercurial-extension-helloworld',
    version='0.1',
    description="Helloworld extension for Mercurial",
    long_description=read('README.rst'),
    package_dir={'': 'src'},
    packages=find_packages('src'),
    author='Shinya Okano',
    author_email='tokibito@gmail.com',
    url='https://github.com/tokibito/mercurial-helloworld',
    install_requires=['Mercurial'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
    ])
