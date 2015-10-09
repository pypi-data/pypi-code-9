try:
  from setuptools import setup
except:
  from distutils.core import setup

config = {
    'description': "Compute entropy, Shannon's information and several related quantities",
    'author': 'Pablo Jadzinsky and Lane McIntosh',
    'url': 'https://github.com/baccuslab/shannon.git',
    'download_url': 'https://github.com/baccuslab/shannon/tarball/0.1',
    'author_email': 'pjadzinsky@gmail.com;lmcintosh@stanford.edu',
    'version': '0.1',
    'install_requires': ['nose', 'numpy', 'scipy'],
    'packages': [],
    'py_modules': ['discrete', 'continuous', 'bottleneck'],
    'scripts': [],
    'name': 'shannon'
    }

setup(**config)
