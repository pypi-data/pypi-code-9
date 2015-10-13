from setuptools import setup, find_packages

setup(
    name="await",
    version="0.1.0",
    author="Madison May",
    author_email="madison@indico.io",
    packages=find_packages(),
    install_requires=[
        "futures >= 2.2.0",
        "dill >= 0.2.3",
        "gevent == 1.0.1"
    ],
    description="""
        Minimalist decorators for asynchronous control flow.
    """,
    license="MIT License (See LICENSE)",
    long_description=open("README.rst").read(),
    url="https://github.com/madisonmay/await"
)
