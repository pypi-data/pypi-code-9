from setuptools import setup, find_packages
import sys

PY_VERSION = sys.version_info[:2]
PY2 = (PY_VERSION[0] == 2)
PY3 = (PY_VERSION[0] == 3)

requirements = []

if sys.version_info[:2] == (2, 6):
    requirements.append('ordereddict')

package_version = '0.5.7'

setup(
    name='pyvagrantfile',
    packages=find_packages(exclude=['tests*']),
    version=package_version,
    description='Parser to extract data from a Vagrantfile into a data struct readable by python',
    long_description='README.rst',
    author='Drew J. Sonne',
    author_email='drew.sonne@gmail.com',
    url='https://github.com/drewsonne/pyvagrantfile',
    download_url='https://github.com/drewsonne/pyvagrantfile/archive/{0}.tar.gz'.format(package_version),
    include_package_data=True,
    install_requires=requirements,
    keywords=['vagrant', 'parser', 'ruby'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development',
        'Topic :: System :: Installation/Setup'
    ]
)
