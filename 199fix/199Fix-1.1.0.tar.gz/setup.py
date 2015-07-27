from distutils.core import setup
from setuptools import find_packages
import i99fix

setup(
    name=i99fix.__app_name__,
    packages=find_packages(exclude=('tests',)),
    version=i99fix.__version__,
    author='Madra David',
    author_email='madra@199fix.com',
    url=i99fix.__app_url__,
    download_url='https://github.com/199fix/199fix/tarball/0.1',
    description='199fix exception logger for Django',
    license='MIT',
    long_description=open('README.rst').read(),
    install_requires=['Django>=1.4'],
    keywords=['logging', 'uptime monitoring'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
)