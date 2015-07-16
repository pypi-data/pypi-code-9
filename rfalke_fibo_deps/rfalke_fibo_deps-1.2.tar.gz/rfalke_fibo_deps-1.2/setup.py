from setuptools import setup, find_packages

setup(
    name="rfalke_fibo_deps",
    version="1.2",
    packages=find_packages(),
    install_requires = ['sh>=1.11']
)
