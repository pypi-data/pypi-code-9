#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'Cython',
    'numpy',
    'scipy',
    'matplotlib',
    'ez_setup',
    'fipy',
    'ciabatta',
    'spatious',
    'fealty',
    'agaro',
    'metropack',
]

test_requirements = [
    'Cython',
    'numpy',
    'scipy',
    'matplotlib',
    'ez_setup',
    'fipy',
    'ciabatta',
    'spatious',
    'fealty',
    'agaro',
    'metropack',
]

extensions = cythonize([
    Extension("ahoy.numerics", ["ahoy/numerics.pyx"],
              include_dirs=[numpy.get_include()]),
])

console_scripts = [
    'plot_chi_uds_x = ahoy.utils.scripts:plot_chi_uds_x',
    'plot_Dr_0_Ds_scalar = ahoy.utils.scripts:plot_Dr_0_Ds_scalar',
    'plot_linear_density = ahoy.utils.scripts:plot_linear_density',
    'plot_p_0_Ds_scalar = ahoy.utils.scripts:plot_p_0_Ds_scalar',
    'plot_pf_Ds_scalar = ahoy.utils.scripts:plot_pf_Ds_scalar',
    'plot_pf_uds_x = ahoy.utils.scripts:plot_pf_uds_x',
    'plot_t_Ds_scalar = ahoy.utils.scripts:plot_t_Ds_scalar',
    'plot_t_Ds_vector = ahoy.utils.scripts:plot_t_Ds_vector',
    'plot_t_rs_scalar = ahoy.utils.scripts:plot_t_rs_scalar',
    'plot_t_rs_vector = ahoy.utils.scripts:plot_t_rs_vector',
    'plot_t_u_nets_scalar = ahoy.utils.scripts:plot_t_u_nets_scalar',
    'plot_t_u_nets_vector = ahoy.utils.scripts:plot_t_u_nets_vector',
    'plot_t_uds_scalar = ahoy.utils.scripts:plot_t_uds_scalar',
    'plot_t_uds_vector = ahoy.utils.scripts:plot_t_uds_vector',
    'plot_vis = ahoy.utils.scripts:plot_vis',
]

setup(
    name='ahoy',
    version='0.4.3',
    description="Agent-based simulations of active particles",
    long_description=readme + '\n\n' + history,
    author="Elliot Marsden",
    author_email='elliot.marsden@gmail.com',
    url='https://github.com/eddiejessup/ahoy',
    packages=setuptools.find_packages(exclude=['docs', 'tests']),
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='ahoy',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    ext_modules=extensions,
    entry_points={
        'console_scripts': console_scripts,
    }
)
