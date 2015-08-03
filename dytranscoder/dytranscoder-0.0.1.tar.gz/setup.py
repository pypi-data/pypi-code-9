#!/usr/bin/env python

from setuptools import setup, find_packages
from dytranscoder import VERSION

url="http://git.hoge.cn/jeffkit/dytranscoder-py"

long_description="Da yang transcoder Python SDK"

setup(name="dytranscoder",
      version=VERSION,
      description=long_description,
      maintainer="jeff kit",
      maintainer_email="jeffkit@hoge.cn",
      url = url,
      long_description=long_description,
      install_requires = ['requests', 'xmltodict', 'dicttoxml'],
      packages=find_packages('.'),
     )
