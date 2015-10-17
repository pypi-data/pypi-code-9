# -*- coding: utf-8 -*-
from setuptools import setup

description = """
django-compressor compressor for react
"""

setup(
    name='django_compress_react',
    version='0.0.2',
    description=description,
    long_description=description,
    author='tekton',
    author_email='tyler@pyroturtle.com',
    url='https://github.com/tekton/django-compress-react',
    packages=["compress_react"],
    zip_safe=False,
    install_requires=["PyReact", "django-compressor"],
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
    ]
)
