from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open("requirements.txt", "r") as requirements_file:
    requirements = [x.strip() for x in requirements_file.readlines()]

scripts = (
    'scripts/cl_load_job',
    'scripts/pdbclean',
    'scripts/pdbsplitsegs',
    'scripts/srmsd',
    'scripts/cluspro_local.py',
    'scripts/cluster.py',
    'scripts/ftrmsd.py',
    'scripts/pwrmsd.py',
)

with open(path.join(here, "README.md")) as f:
    long_description = f.read()

setup(
    name="sblu",
    version="0.2.0",
    packages=['sblu'],
    description="Library for munging data files from ClusPro/FTMap/etc.",
    long_description=long_description,

    url="https://bitbucket.org/bu-structure/sb-lab-utils",

    author="Bing Xia",
    author_email="sixpi@bu.edu",

    license="MIT",

    install_requires=requirements,

    scripts=scripts,

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],

    keywords='cluspro protein PDB',

    use_2to3=True,
)
