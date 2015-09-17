

from setuptools import setup, find_packages

import pynrfjprog

setup(
    
    name ='pynrfjprog',
        
    version = pynrfjprog.__version__,
    
    description = 'A simple Python interface for the nrfjprog.dll',
    long_description = 'A simple Python interface for the nrfjprog.dll. Since nrfjprog.dll is a 32 bit windows application, this package can only be used with windows and 32bit Python 2.7.x',
    
    url = 'http://www.nordicsemi.com/',
        
    author = 'Nordic Semiconductor ASA',
    
    license = 'BSD',
    
    classifiers = [

        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',

        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Debuggers',
        
        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
    
    keywords = 'nrfjprog pynrfjprog',
     
    install_requires = ['enum34'],
     
    packages = find_packages(),
    package_data = { 
                'pynrfjprog': ['*.dll'],
                'pynrfjprog.docs': ['*.h'],
                'pynrfjprog.examples': ['*.hex']
    }
    
    )