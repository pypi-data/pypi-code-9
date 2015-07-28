from distutils.core import setup, Extension

module1 = Extension('systime',
                    sources = ['systimemodule.c'])

setup (name = 'SysTime',
       version = '1.0',
       description = 'This is a package that allows you to set system time',
       author = 'Eric Li',
       ext_modules = [module1])
