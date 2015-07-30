from setuptools import setup,find_packages


# Declare your packages' dependencies here, for eg:
requires=[
            'cmd2==0.6.7',
            'argparse',
            'progressbar==2.3',
            'termcolor==1.1.0'
         ]
    
                    
setup (
  install_requires=requires,
  
  name = 'ussclicore',
  version = '1.0.2',
  description='UShareSoft cli core module',
  #long_description='',
  packages = find_packages(),
  author = 'Joris Bremond',
  author_email = 'joris.bremond@usharesoft.com',
  license="Apache License 2.0",
  #url = '',
  classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
       
  
  #long_description= 'Long description of the package',
  
)
