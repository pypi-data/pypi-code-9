"""
Microsatellites-Finder
======================

This Python package searches for microsatellites in fasta sequences. It can both find perfect or
imperfect repeats.
The available options are the following:

- `-i, --input-fasta`: path of the fasta file containing the sequence(s) to analyze. The file can be
either a plain text file or a gzip compressed file.
- `-o, --output-file`: path of the file to save with the results of the analysis. The coordinates of
the microsatellites will be 0-based.
- `-l, --seed-length`: length of the seed of the microsatellites, i.e. the number of nucleotides
that will be repeated. For instance `-l 2` will find microsatellites like `ACACACAC` where the seed
`AC` is repeated 4 times.
- `-r, --minimum_repetitions`: minimum number of repetitions of the seed. For instance `-r 3` will
find microsatellites like `CTACTACTA` or `CTACTACTACTA` where the seed `CTA` is repeated at least 3
times. The minimum allowed value is 2 and the default value is 3.
- `-im, --imperfect`: include imperfect microsatellites. With this option microsatellites repeated
at least `-r -1` times that share the same seed and have a distance up to the "--imperfect" value
will be merged together and will be considered as a single microsatellite. By default this option is
disabled and microsatellites are kept separated.
- `-s, --strict`: when `--imperfect` is a positive integer, this option allows to search for
imperfect microsatellites only by using nucleotides that are present in the seed. For instance, if
the seed is `AT` only the nucleotides `A` and `T` will be considered. By default this option is
disabled and all the nucleotides `ACGT` are considered.
- `-a, --alphabet`: alphabet to use for the microsatellites search. The alphabet can be either "dna"
for DNA or "aa" for PROTEINS. Default is "dna".
- `-f, --flanking`: length of the sequences flanking the microsatellites. The sequences will be
written in the output file. Sequences that overstep the boundaries of a chromosome will be
truncated. By default this option is disabled.
- `-c, --cores`: number of CPUs to use in the computation. By default it will use all the available
CPUs.
- `-p, --progress`: track the progress of the computation with a progress bar.
"""


__author__ = 'Loris Mularoni'


# Import modules
from setuptools import setup, find_packages
from micros_finder import __version__


setup(
    name='microsatellites_finder',
    version=__version__,
    packages=find_packages(exclude=['tests*']),
    # package_data={'microsatellites_finder': ['data/*.gz', 'data/*.txt']},
    include_package_data=True,
    url='https://bitbucket.org/batterio/microsatellites_finder/',
    download_url="https://bitbucket.org/batterio/microsatellites_finder/get/{}.tar.gz".format(__version__),
    license='The MIT License (MIT)',
    author=__author__,
    author_email='loris.mularoni@gmail.com',
    description='Python package that searches for microsatellites in fasta sequences',
    classifiers=['Programming Language :: Python :: 3.4'],
    keywords='repeats, microsatellites',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'find_micro = micros_finder.find_microsatellites:main'
        ]
    }
)
