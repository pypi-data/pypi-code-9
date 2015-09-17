# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
        name='docutils_react_docgen',
        version='1.1.0',
        description="docutils extension which converts react-docgen output to restructured text",
        long_description=open('README.rst', 'r').read(),
        author='Paul Wexler',
        author_email="paul@prometheusresearch.com",
        license="MIT",
        url='https://bitbucket.org/pwexler/docutils_react_docgen',
        classifiers=[
                'Programming Language :: Python',
                'Intended Audience :: Developers',
                 ],
        platforms='Any',
        keywords=('docutils', 'sphinx', 'react', 'docgen', 'documentation'),
        package_dir={'': 'src'},
        packages=find_packages('src'),
        install_requires=[
                'sphinx-rtd-theme>=0.1.7, <1',
                ] 
        )

