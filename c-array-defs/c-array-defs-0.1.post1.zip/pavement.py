import sys

from paver.easy import task, needs, path, sh, cmdopts, options
from paver.setuputils import setup, install_distutils_tasks
from distutils.extension import Extension
from distutils.dep_util import newer

sys.path.insert(0, path('.').abspath())
import version

setup(name='c-array-defs',
      version=version.getVersion(),
      description='Simple C classes for arrays of standard numeric types.',
      keywords='c++ array simple',
      author='Christian Fobel',
      author_email='christian@fobel.net',
      url='https://github.com/wheeler-microfluidics/c-array-defs',
      license='GPL',
      packages=['c_array_defs', ],
      # Install data listed in `MANIFEST.in`
      include_package_data=True)


@task
def build_arduino_library():
    import os
    import tarfile

    arduino_lib_dir = path('c_array_defs').joinpath('lib')
    if not arduino_lib_dir.isdir():
        arduino_lib_dir.mkdir()
    tf = tarfile.TarFile.bz2open(arduino_lib_dir
                                 .joinpath('C-Array-Defs.tar.gz'), 'w')
    for s in path('c_array_defs').joinpath('Arduino', 'CArrayDefs').files():
        tf.add(s, os.path.join('CArrayDefs', s.name))
    tf.close()


@task
@needs('generate_setup', 'minilib', 'build_arduino_library',
       'setuptools.command.sdist')
def sdist():
    """Overrides sdist to make sure that our setup.py is generated."""
    pass
