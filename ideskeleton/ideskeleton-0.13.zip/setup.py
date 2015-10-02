from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='ideskeleton',
      version='0.13',
      description="Scaffolding of IDE project files such as Visual Studio from Python existing" \
          "folder structure",
      long_description=readme(),
      author="Javier Ruiz Aranguren",
      license="MIT",
      url="http://github.com/jruizaranguren/ideskeleton",
      packages=['ideskeleton'],
      include_package_data=True,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Topic :: Text Editors :: Integrated Development Environments (IDE)'
          ]
      )

__author__ = "Javier Ruiz Aranguren"