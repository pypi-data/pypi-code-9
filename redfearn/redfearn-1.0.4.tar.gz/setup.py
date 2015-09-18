from setuptools import setup

setup(
    name='redfearn',
    version='1.0.4',
    description="Converts between latitude/longitude and grid coordinates using Redfearn's Formula",
    author='PHil Howarth',
    author_email='phil@plaintech.net.au',
    url='http://plaintech.net.au/redfearn',
    long_description=(
        "A python module to use Redfearn's formula to convert between latitude/longitude pairs and various grid coordinate systems used in Australia."
        "Based on the document titled 'Geocentric Datum of Australia - Technical Manual Version 2.3 Amendment 1' "
        "produced by the 'Intergovernmental Committee on Surveying and Mapping', ISBN 0-9579951-0-5"
    ),
    keywords=["conversion", "GDA", "MGA", "latitude", "longitude"],
    license="GPLv3+",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
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
    py_modules=['redfearn', 'tests']
)
