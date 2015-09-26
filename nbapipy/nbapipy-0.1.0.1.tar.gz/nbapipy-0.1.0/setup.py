import os
from distutils.core import setup
from setuptools import find_packages

packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)
for dirpath, dirnames, filenames in os.walk('nbapipy'):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[12:] # Strip "admin_tools/" or "admin_tools\"
        for f in filenames:
            data_files.append(os.path.join(prefix, f))

setup(
    name="nbapipy",
    version="0.1.0",
    author="Raul Gil",
    author_email="gilraul90@gmail.com",
    url='http://github.com/rgil90/nbapipy',
    # license="LICENSE.txt",
    summary="API wrapper around the erikberg web service",
    description="API wrapper around the erikberg mlb/nba web service",
    package_dir={'nbapipy': 'nbapipy'},
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3.4',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: Public Domain',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Development Status :: 3 - Alpha',
    ]
)
