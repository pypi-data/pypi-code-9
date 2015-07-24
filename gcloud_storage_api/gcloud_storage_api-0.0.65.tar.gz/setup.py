import os
from setuptools import setup

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

setup(
  name = 'gcloud_storage_api',
  packages = ['gcloud_storage_api'],
  version = '0.0.65',
  install_requires=['requests','argparse'],
  description = 'gCloud - The Cloud made in Italy Python API',
  long_description=(read('Docs/ABOUT.rst' ) + '\n\n' +
                    '\n\n------------\n\n' +
                    read('Docs/INSTALL.rst') + '\n\n' +
                    '\n\n------------\n\n' +
                    read('Docs/GCLOUD_REPOSITORY.rst' ) + '\n\n' +
                    '\n\n------------\n\n' +
                    read('Docs/HOW_TO_USE.rst') + '\n\n' +
                    '\n\n------------\n\n' +
                    read('Docs/SC31.rst') + '\n\n' +
                    #read('Docs/EXAMPLE.rst') + '\n\n' +
                    ' '),
  author = 'Ilario Febi',
  author_email = 'ifebi@schema31.it',
  url = 'http://gcloud.schema31.it',
  license = 'BSD',
  keywords = ['gcloud', 'schema31', 'Schema 31'], 
  classifiers=[ 'Development Status :: 3 - Alpha',
                'Intended Audience :: Developers',
                'Natural Language :: Italian',
                'License :: OSI Approved :: BSD License',
                'Operating System :: OS Independent',
                'Programming Language :: Python',
                'Programming Language :: Python :: 2',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3',
                'Programming Language :: Python :: 3.4',
                'Environment :: Console',
  ],
  entry_points={
    'console_scripts': [
        'gcloud_storage=gcloud_storage_api.Cloud31_Storage31:main',
    ],
  },
)
