# encoding=utf-8

from setuptools import setup


setup(
    name="megalamp_test",
    version="0.19",
    author="Panaetov Alexey",
    author_email="panaetovaa@gmail.com",
    description=(
        "Test model of mega lamp"
    ),
    license = "BSD",
    url = "https://bitbucket.org/panaetov/megalamp",
    packages=['megalamp'],
    keywords = "python tornado",
    install_requires=['tornado'],
    classifiers=[],
    entry_points="""
    # ...
    [console_scripts]
    megalamp = megalamp:main
    """,
)
