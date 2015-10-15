#!/usr/bin/env python

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from subprocess import call

from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext

class ImmunioBuild(build_ext):
    def run(self):
        """ First pre-build the require static library:

            "immunio/lua-hooks/ext/luajit/src/libluajit.a"
        """
        args = ["make", "-C", "immunio/lua-hooks", "ext/luajit/src/libluajit.a"]
        self.execute(call, [args], "Building libluajit.a")

        build_ext.run(self)

setup(name='immunio',
      version='0.34.0',
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
          extra_compile_args=[b'-DLUA_USE_APICHECK',
                              b'-DLUAJIT',
                              b'-Dlua_assert=assert',
                              b'-O3',
                              b'-fPIC'],
          extra_objects=[b'immunio/lua-hooks/ext/luajit/src/libluajit.a'],
          include_dirs=[b'immunio/lua-hooks/ext',
                        b'immunio/lua-hooks/ext/luajit/src/'],
      )],
      classifiers=[
          "Framework :: Django",
          "Framework :: Flask",
          "Framework :: Pyramid",
          "Intended Audience :: Developers",
          "License :: Other/Proprietary License",
          "Topic :: Security",
      ],

      cmdclass={"build_ext": ImmunioBuild},
)
