from setuptools import setup
import os
import re


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('emotient')


setup(
    name='emotient',
    version=version,
    description='Use the Emotient Analytics APIs from Python',
    url='https://github.com/emotient/emotient-python',
    author='Emotient',
    author_email='support@emotient.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='emotient',
    packages=['emotient'],
    install_requires=[
        'python-dateutil>=2.4.2',
        'requests>=2.7.0',
        'six>=1.9.0'
    ],
)
