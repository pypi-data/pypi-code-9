# -*- coding: utf-8 -*-
#from distutils.core import setup
from setuptools import setup
setup (
    name='denden_extension',
    version='0.1.0',
    description='Python-Markdown extention for Den-Den Markdown',
    url='https://github.com/muranamihdk/denden_extension',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Documentation',
        'Topic :: Text Processing :: Markup',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Japanese',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='markdown denden-markdown Japanese epub ruby',
    py_modules=['denden_extension'],
    install_requires=['markdown>=2.6'],
)

