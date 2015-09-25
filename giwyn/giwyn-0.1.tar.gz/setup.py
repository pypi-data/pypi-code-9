from setuptools import setup

setup(name='giwyn',
      version='0.1',
      description='A simple command to manage all your git clones',
      url='http://github.com/k0pernicus/giwyn',
      author='k0pernicus',
      author_email='antonin.carette@gmail.com',
      license='GnuGPL',
      packages=['giwyn'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'Programming Language :: Python :: 3.4'
      ],
      keywords='git development versioning package',
      install_requires=['gitpython'],
      zip_safe=False)
