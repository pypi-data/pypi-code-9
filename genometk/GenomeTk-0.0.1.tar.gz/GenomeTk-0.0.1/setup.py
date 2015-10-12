from distutils.core import setup

import os


def version():
    setupDir = os.path.dirname(os.path.realpath(__file__))
    versionFile = open(os.path.join(setupDir, 'genome_tk', 'VERSION'))
    return versionFile.read().strip()

setup(
    name='GenomeTk',
    version=version(),
    author='Donovan Parks',
    author_email='donovan.parks@gmail.com',
    packages=['genome_tk'],
    scripts=['bin/genome_tk'],
    package_data={'genome_tk' : ['VERSION'], '': ['distributions/*.txt']},
    url='http://pypi.python.org/pypi/genome_tk/',
    license='GPL3',
    description='A toolbox for working with genomes.',
    long_description=open('README.md').read(),
    install_requires=[
        "numpy >= 1.8.0",
        "biolib >= 0.0.11"],
)
