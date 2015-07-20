from setuptools import setup
import versioneer

project_name = 'phconvert'

## Configure versioneer
versioneer.VCS = 'git'
versioneer.versionfile_source = project_name + '/_version.py'
versioneer.versionfile_build = project_name + '/_version.py'
versioneer.tag_prefix = '' # tags are like 1.2.0
versioneer.parentdir_prefix = project_name + '-'


## Metadata
long_description = """
phconvert
==========

Convert and write `Photon-HDF5 <http://photon-hdf5.org/>`_ files.

"""

setup(name = project_name,
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      author = 'Antonino Ingargiola',
      author_email = 'tritemio@gmail.com',
      url          = 'http://photon-hdf5.github.io/phconvert/',
      download_url = 'http://photon-hdf5.github.io/phconvert/',
      install_requires = ['numpy', 'setuptools', 'tables', 'matplotlib', 'future'],
      license = 'MIT',
      description = ("Convert and write Photon-HDF5 files."),
      long_description = long_description,
      platforms = ('Windows', 'Linux', 'Mac OS X'),
      classifiers=['Intended Audience :: Science/Research',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3.4',
                   'Topic :: Scientific/Engineering',
                   ],
      packages = ['phconvert'],
      package_data = {'phconvert': ['specs/*.json']},
      keywords = ('single-molecule FRET smFRET biophysics file-format HDF5 '
                  'Photon-HDF5'),
      )

