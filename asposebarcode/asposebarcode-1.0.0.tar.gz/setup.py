__author__ = 'imranwar'

from setuptools import setup, find_packages

setup(
    name = 'asposebarcode',
    packages = find_packages(),
    version = '1.0.0',
    description = 'Aspose Cloud SDK for Python allows you to use Aspose API in your Python applications',
    author='Imran Anwar',
    author_email='imranwar@gmail.com',
    url='https://github.com/asposebarcode/Aspose_BarCode_Cloud/tree/master/SDKs/Aspose.BarCode_Cloud_SDK_for_Python',
    install_requires=[
        'asposestorage',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
