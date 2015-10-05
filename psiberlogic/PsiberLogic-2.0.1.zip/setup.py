from setuptools import setup, find_packages
setup(
      name = 'PsiberLogic',
      packages = ['PsiberLogic','PsiberLogic.demo'], # this must be the same as the name above
      version = '2.0.1',
      description = 'A speed-optimized, barebones, Python 3 fuzzy controller package.',
      author = 'Psibernetix Inc.',
      author_email = 'contact@psibernetix.com',
      keywords = 'Fuzzy Logic',
	  license = 'GNU Library or Lesser General Public License (LGPL)',
	  url = "http://packages.python.org/psiberlogic",
	  install_requires = ['numpy'],
	  package_data = {'': ['*.pyx','*.c','*.pyd','*.txt']},
	  classifiers = [
	  'Development Status :: 4 - Beta',
	  'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
	  'Programming Language :: Python :: 3',
	  'Intended Audience :: Developers',
	  'Intended Audience :: Education',
	  'Intended Audience :: Science/Research',
      'Topic :: Scientific/Engineering',
	  ],
)