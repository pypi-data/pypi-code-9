from setuptools import setup,find_packages

setup(
    name='ksr',
    version='0.1.5',
    py_modules=['ksr'],
    url='https://github.com/jedahan/kickstarter',
    description='commandline kickstarter',
    author='Jonathan Dahan',
    author_email='jonathan@jonathan.is',
    license='ISC',
    install_requires=[
        'Click',
        'TinyDB',
    ],
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: Console',
      'License :: OSI Approved :: ISC License (ISCL)',
      'Natural Language :: English',
      'Operating System :: MacOS :: MacOS X',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.5',
      'Topic :: Software Development :: User Interfaces',
      'Topic :: Utilities',
    ],
    entry_points='''
        [console_scripts]
        ksr=ksr:cli
    ''',
    packages=find_packages(),
    keywords = ['kickstarter'],
    download_url = 'https://github.com/jedahan/kickstarter/tarball/0.1.3',
)
