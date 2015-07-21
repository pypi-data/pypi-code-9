from distutils.core import setup
setup(name='indexedzodb',
      version='0.0.8',
      license='MIT',
      description='A simple, indexed model layer over ZODB',
      author='Mark Skelton',
      author_email='mark@software13.co.uk',
      url='https://github.com/mtskelton/indexedzodb/',
      py_modules=['indexedzodb.models'],
      install_requires=['ZODB', 'zodbpickle', 'repoze.catalog'],
      requires=['ZODB', 'zodbpickle'],
      data_files=['LICENSE', 'README.md'],
      provides=['indexedzodb'],
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'License :: OSI Approved :: MIT License',
                   'Topic :: Database :: Front-Ends',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   ]
      )
