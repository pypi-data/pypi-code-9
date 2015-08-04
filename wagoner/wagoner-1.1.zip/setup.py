"""
Setup module for wagoner.
"""

from setuptools import setup, find_packages

with open("README.rst", "r") as readme:
    setup(
        name="wagoner",
        version="1.1",
        description="A random word generator.",
        long_description=readme.read(),
        url="https://github.com/sbusard/wagoner",
        author="Simon Busard",
        author_email="simon.busard@gmail.com",
        license="MIT",
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Topic :: Utilities",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.4"
        ],
        keywords="random word generation",
        packages=find_packages(),
        scripts=[
            "wagoner/table.py",
            "wagoner/tree.py",
            "wagoner/word.py"
        ]
    )
