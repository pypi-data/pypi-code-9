from setuptools import setup, find_packages

__version__ = "0.3.0"

setup(
    name='bgconvert',
    version=__version__,
    packages=find_packages(),
    package_data={'bgconvert.datasets': ['*.xz']},
    url="https://bitbucket.org/bgframework/bgconvert",
    download_url="https://bitbucket.org/bbglab/bgconvert/get/"+__version__+".tar.gz",
    license='Apache Commons 2.0',
    author='Biomedical Genomics Group',
    description='',
    install_requires=[]
)
