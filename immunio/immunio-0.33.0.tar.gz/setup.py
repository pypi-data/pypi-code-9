#!/usr/bin/env python

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from setuptools import setup, find_packages, Extension


setup(name='immunio',
      version='0.33.0',
      description='Immunio agent library',
      author='Immunio',
      author_email='contact@immun.io',
      url='https://www.immun.io',
      packages=find_packages(exclude=["tests", "tests.*"]),
      include_package_data=True,
      use_2to3=True,
      ext_modules=[Extension(
          b'immunio.deps.lupa._lupa',
          sources=[
              b'immunio/deps/lupa/_lupa.c',
              b'immunio/lua-hooks/ext/all.c',
              b'immunio/lua-hooks/ext/libinjection/libinjection_html5.c',
              b'immunio/lua-hooks/ext/libinjection/libinjection_xss.c',
              b'immunio/lua-hooks/ext/libinjection/libinjection_sqli.c',
              b'immunio/lua-hooks/ext/lpeg/lpcap.c',
              b'immunio/lua-hooks/ext/lpeg/lpcode.c',
              b'immunio/lua-hooks/ext/lpeg/lpprint.c',
              b'immunio/lua-hooks/ext/lpeg/lpvm.c',
          ],
          include_dirs=[b'immunio/lua-hooks/ext', b'immunio/lua-hooks/ext/lua'],
      )],
      classifiers=[
          "Framework :: Django",
          "Framework :: Flask",
          "Framework :: Pyramid",
          "Intended Audience :: Developers",
          "License :: Other/Proprietary License",
          "Topic :: Security",
      ],
)
