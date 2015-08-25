import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()


def get_requires_from_txt(filename):
    requires = []
    with open(os.path.join(here, filename)) as f:
        for line in f:
            if not line.startswith('--'):
                requires.append(line.replace('\n', ''))

    return requires


setup(name='launchkey-twisted',
      version='1.0.0',
      description='LaunchKey Asynchronous SDK for Twisted',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Twisted",
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      author='LaunchKey',
      author_email='support@launchkey.com',
      url='https://launchkey.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=False,
      test_suite='nose.collector',
      install_requires=['six', 'twisted', 'pyOpenSSL', 'service_identity', 'launchkey-python'],
      tests_require=['unittest2', 'nose', 'coverage'],
      )
