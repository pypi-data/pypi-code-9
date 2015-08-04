"""
OBD Library
-------------

A Python interface to OBD-II scanners

"""
from setuptools import setup

setup(
    name="obdlib",
    version="0.2",
    license="MIT",
    author="Siarhei Boika",
    author_email="s.s.boika@gmail.com",
    description="OBD Library",
    long_description=__doc__,
    packages=["obdlib", "obdlib.obd", "obdlib.obd.protocols"],
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=[
        "pyserial>=2.7"
    ],
    tests_require=[
        "nose",
    ],
    test_suite='nose.collector',
    keywords=['obd', 'obdii', 'automotive'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Communications",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
        "Topic :: Utilities"
    ]
)
