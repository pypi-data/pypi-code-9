# -*- coding: utf-8 -*-

import os
import re

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, "__init__.py")).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)

setup(
    name="djangocms-restapi",
    version=get_version("djangocms_restapi"),
    description="REST api interface for Django CMS",
    long_description="REST api interface for Django CMS based on Django REST Framework",
    author="Rolf Håvard Blindheim",
    author_email="rolf.blindheim@inonit.no",
    url="https://github.com/inonit/djangocms-restapi",
    download_url="https://github.com/inonit/djangocms-restapi.git",
    license="MIT License",
    packages=[
        "djangocms_restapi",
    ],
    include_package_data=True,
    install_requires=[
        "Django>=1.7.0",
        "djangorestframework>=3.1.0",
        "djangorestframework-recursive>=0.1.1",
        "django-cms>=3.1.0"
    ],
    tests_require=[
        "nose",
        "mock",
        "coverage",
    ],
    zip_safe=False,
    test_suite="tests.runtests.start",
    classifiers=[
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
