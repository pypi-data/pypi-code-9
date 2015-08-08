import os
import re
import codecs
from setuptools import setup, find_packages


def read(*parts):
    filename = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(filename, encoding='utf-8') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

requires = [
    'six',
]
extras = {
    'database': ['django-picklefield'],
    'redis': ['redis'],
    'mongo': ['pymongo>=3.0.1'],
}

setup(
    name='waterboy',
    version=find_version("waterboy", "__init__.py"),
    url="http://github.com/gmflanagan/waterboy",
    description='Live application settings with pluggable backends, including Redis and MongoDB.',
    long_description=read('README.rst'),
    author='Jerd Flanagan',
    author_email='gmflanagan@outlook.com',
    license='BSD',
    keywords='libraries settings redis mongodb'.split(),
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities',
    ],
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    extras_require=extras,
)
