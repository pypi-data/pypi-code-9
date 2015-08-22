from distutils.core import setup
import os

def read(*paths):
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


setup(
    name='Js2Py',
    version='0.27',
    packages=['js2py', 'js2py.utils', 'js2py.prototypes', 'js2py.translators', 'js2py.constructors', 'js2py.host'],
    url='https://github.com/PiotrDabkowski/Js2Py',
    install_requires = ['tzlocal>=1.2'],
    license='GPL',
    author='Piotr Dabkowski',
    author_email='piotr.dabkowski@balliol.ox.ac.uk',
    description='JavaScript to Python Translator & JavaScript interpreter written in 100% pure Python.',
    long_description=read('README.rst')
)
