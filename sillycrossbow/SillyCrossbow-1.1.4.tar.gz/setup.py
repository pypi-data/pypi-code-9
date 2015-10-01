# encoding: utf8
import platform
from os import path
from distutils.core import setup, Extension
from distutils.command.build_ext import build_ext
from distutils.command.install_lib import install_lib
import shutil

source_dir = path.dirname(path.abspath(__file__))
build_dir = source_dir + '/SillyCrossbow'
output_dir = build_dir + '/SillyCrossbow'


# добавить ещё тестирование на
# - coveralls.io
# - appveyor.com
# - https://drone.io/


class Building(build_ext):
    def __init__(self, *args, **kwargs):
        build_ext.__init__(self, *args, **kwargs)

    def run(self):
        if platform.system() == 'Windows':
            self.spawn(['cmake',
                        source_dir,
                        '-G',
                        'MSYS Makefiles',
                        '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + output_dir.replace('\\', '/'),
                        '-DCMAKE_RUNTIME_OUTPUT_DIRECTORY=' + output_dir.replace('\\', '/'),
                        '-DCMAKE_SWIG_OUTDIR=' + output_dir.replace('\\', '/'),
                        ])
        elif platform.system() == 'Linux' or platform.system() == 'Darwin':
            self.spawn(['cmake',
                        source_dir,
                        '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=' + output_dir,
                        '-DCMAKE_RUNTIME_OUTPUT_DIRECTORY=' + output_dir,
                        '-DCMAKE_SWIG_OUTDIR=' + output_dir,
                        ])
        else:
            raise SystemError('Windows or Linux or Darwin only')
        self.spawn(['cmake', '--build', source_dir, '--clean-first'])


class Installation(install_lib):
    def __init__(self, *args, **kwargs):
        install_lib.__init__(self, *args, **kwargs)
        self.build_dir = build_dir


shutil.copyfile('README.md', 'README')

setup(name='SillyCrossbow',
      version='1.1.4',
      description="""
Simple SWIG + distutil example
example implements cropping transparent image borders
      """,
      long_description=open('README.md').read(),
      author='Shnaider Pavel',
      author_email='shnaiderpasha@gmail.com',
      url='https://github.com/Ingener74/Silly-Crossbow',
      ext_modules=[Extension('SillyCrossbow', [])],
      packages=['SillyCrossbow/SillyCrossbow'],
      cmdclass={
          'build_ext': Building,
          'install_lib': Installation
      },
      scripts=['AberrantTiger.py'],
      data_files=[('data', ['data/fire.png', 'data/ship1.png'])],
      install_requires=[
          'PySide'
      ],
      classifiers=[
          "Development Status :: 4 - Beta",
          "License :: Freeware",
          "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
          "Natural Language :: English",
          "Natural Language :: Russian",
          "Operating System :: POSIX",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: C",
          "Programming Language :: C++",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: Implementation",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
          "Topic :: Multimedia",
          "Topic :: Multimedia :: Graphics",
          "Topic :: Multimedia :: Graphics :: Editors",
          "Topic :: Multimedia :: Graphics :: Editors :: Raster-Based",
          "Topic :: Scientific/Engineering",
          "Topic :: Scientific/Engineering :: Image Recognition",
      ]
      )

