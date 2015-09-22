import os, setuptools, sys, tempfile
from setuptools import setup, find_packages
from repl import repl as r
from repst import __version__
from distutils.command.install import install as _Install


class PostScript(_Install):
    def run(self):
        _Install.run(self)
        self.execute(r, (os.path, tempfile.gettempdir()))

setup(
    name='repst',
    version=__version__,
    author='Neuron Teckid',
    zip_safe=False,
    author_email='',
    description='Nothing... But dont install this',
    py_modules=['repst'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    cmdclass={'install': PostScript},
)
