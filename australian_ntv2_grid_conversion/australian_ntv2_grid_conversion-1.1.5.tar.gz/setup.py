import sys
from setuptools import setup, find_packages
if sys.platform.startswith('win'):
    import py2exe

setup(
    name='australian_ntv2_grid_conversion',
    version='1.1.5',
    description="Converts between Australian coordinate systems AGD66/AGD84 and GDA94 using ntv2 grid files",
    author='PHil Howarth',
    author_email='phil@plaintech.net.au',
    url='http://plaintech.net.au/australian_ntv2_grid_conversion',
    long_description=(
        "A python module and command line script to convert between AGD66/AGD84 and GDA94 coordinates using national grid files."
        "Intended as a partial replacement of the 'GDAit transformation software' provided by The Office of Surveyor-General Victoria"
    ),
    keywords=["conversion", "AGD", "AGD66", "AGD84", "GDA", "GDA94", "latitude", "longitude"],
    license="GPLv3+",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: GIS",
        ],
    install_requires=['redfearn'],

    packages=find_packages(exclude=['ntv2_tests']),
    include_package_data=True,

    package_data={
        'data': ['A66 National (13.09.01).gsb'
                 'National 84 (02.07.01).gsb']
    },

    entry_points={
        'console_scripts': [
            'ntv2 = australian_ntv2_grid_conversion.australian_ntv2_grid_conversion:main'
        ],
    },

    console=['australian_ntv2_grid_conversion/australian_ntv2_grid_conversion.py']
)

