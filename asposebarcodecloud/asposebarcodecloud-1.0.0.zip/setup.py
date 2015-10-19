__author__ = 'farooq.sheikh'

from setuptools import setup, find_packages

setup(
    name = 'asposebarcodecloud',
    packages = find_packages(),
    version = '1.0.0',
    description = 'Aspose.Barcode Cloud SDK for Python allows you to use Aspose.Barcode APIs in your Python applications',
    author='Farooq Sheikh',
    author_email='farooq.sheikh@aspose.com',
    url='http://www.aspose.com/cloud/barcode-api.aspx',
    install_requires=[
        'asposestoragecloud',
    ],    
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
