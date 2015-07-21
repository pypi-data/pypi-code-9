from distutils.core import setup

setup(
    name='twothirds',
    version='0.0.1',
    author='Vince Knight',
    url='https://github.com/drvinceknight/twothirds',
    author_email=('vincent.knight@gmail.com'),
    packages=['twothirds', 'twothirds.tests'],
    license='The MIT License (MIT)',
    description='Analyse data from two thirds of the average games',
    install_requires=[
        "matplotlib==1.4.3",
        "mock==1.0.1",
        "nose==1.3.7",
        "numpy==1.9.2",
        "pandas==0.16.2",
        "pyparsing==2.0.3",
        "python-dateutil==2.4.2",
        "pytz==2015.4",
        "scipy==0.15.1",
        "seaborn==0.5.1",
        "six==1.9.0",
        "wsgiref==0.1.2",
        "xlrd"
    ],
)
