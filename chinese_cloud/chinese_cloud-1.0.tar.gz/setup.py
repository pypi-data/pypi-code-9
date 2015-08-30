#!/usr/bin/env python2

from distutils.core import setup
from distutils.extension import Extension

setup(
    name='chinese_cloud',
    version='1.0',
    description='A Chinese word cloud',
    author='Lw-Cui',
    author_email='cui@hellolw.com',
    url='https://github.com/Lw-Cui/Chinese_cloud',
    ext_modules=[Extension("chinese_cloud.query_integral_image",
                           ["chinese_cloud/query_integral_image.c"])],
    packages=['chinese_cloud'],
    package_data={'chinese_cloud': ['stopwords']}
)
