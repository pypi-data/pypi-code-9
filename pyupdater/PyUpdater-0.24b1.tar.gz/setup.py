#!/usr/bin/env python

from setuptools import find_packages, setup

import versioneer


with open(u'requirements.txt', u'r') as f:
    required = f.read().splitlines()

cmd_class = versioneer.get_cmdclass()

extra_s3 = 'PyUpdater-s3-Plugin == 2.4'
extra_scp = 'PyUpdater-scp-Plugin == 2.2'
extra_patch = 'bsdiff4 == 1.1.4'

setup(
    name='PyUpdater',
    version=versioneer.get_version(),
    description='Simple App update framwork',
    author='Johny Mo Swag',
    author_email='johnymoswag@gmail.com',
    url='docs.pyupdater.org',
    download_url=('https://github.com/JMSwag/Py'
                  'Updater/archive/master.zip'),
    license='Apache License 2.0',
    extras_require={
        's3': extra_s3,
        'scp': extra_scp,
        'patch': extra_patch,
        'all': [extra_s3, extra_scp, extra_patch]
        },
    zip_safe=False,
    package_data={
        # This includes precompiled bootloaders.
        'pyupdater.vendor.PyInstaller': ['bootloader/*/*'],
        # This file is necessary for rthooks (runtime hooks).
        'pyupdater.vendor.PyInstaller.loader': ['rthooks.dat'],
        },
    include_package_data=True,
    tests_require=['pytest', extra_patch],
    cmdclass=cmd_class,
    install_requires=required,
    packages=find_packages(),
    entry_points="""
    [console_scripts]
    pyupdater=pyupdater.wrapper:main
    """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4'],
    )
