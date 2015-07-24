from distutils.core import setup
from os import path
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.txt'),'r') as f:
    long_description = f.read()

setup(
    name='tornsmtp',
    version='0.1.5',
    packages=['tornado_smtpclient'],
    url='https://github.com/Rustem/tornado-smtpclient.git',
    license='MIT',
    author='xepa4ep',
    keywords = ["tornado", "smtp", "email", "client", "non blocking", "async"],
    author_email='vumhtam@gmail.com',
    description='A non-blocking smtp client to work with tornado-based application',
    install_requires=['tornado>=4.2'],
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Communications :: Email :: Email Clients (MUA)',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],
    long_description=long_description
)
