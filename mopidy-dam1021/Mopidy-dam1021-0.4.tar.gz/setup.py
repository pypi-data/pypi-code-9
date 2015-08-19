from __future__ import unicode_literals


from setuptools import find_packages, setup

import re

def get_version(filename):
    content = open(filename).read()
    metadata = dict(re.findall('__([a-z]+)__ = "([^"]+)"', content))
    return metadata['version']

module_version =  get_version('mopidy_dam1021/__init__.py')

setup(
    name='Mopidy-dam1021',
    version=module_version,
    url='https://github.com/fortaa/mopidy-dam1021',
    license='Apache License, Version 2.0',
    download_url = 'https://github.com/fortaa/mopidy-dam1021/tarball/%s' % module_version,
    author="Forta(a)",
    author_email="fortaa@users.noreply.github.com",
    description='Mopidy extension for controlling volume on a dam1021 DAC',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'setuptools',
        'Mopidy >= 0.19',
        'Pykka >= 1.1',
	'dam1021',
    ],
    entry_points={
        'mopidy.ext': [
            'dam1021 = mopidy_dam1021:Extension',
        ],
    },
    classifiers=[
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Multimedia :: Sound/Audio :: Players',
    ],
)
