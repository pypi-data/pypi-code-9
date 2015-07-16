from setuptools import setup, find_packages

setup(
    name="rfalke_fibo_deps",
    version="1.5",
    packages=find_packages(exclude=["tests"]),
    install_requires = ['sh>=1.11'],
    test_suite = 'tests'
)
