# -*- coding: utf-8 -*-
from setuptools import setup

try:
    from testkernel import cmdclass
except:
    import pip, importlib
    pip.main(['install', 'test-kernel']); cmdclass = importlib.import_module('testkernel').cmdclass
    
setup(
    name='test-kernel',
    version='0.2',
    description='Test custom kernel pip installable!',
    author='John Coady',
    author_email='johncoady@shaw.ca',
    license='New BSD License',
    url='https://github.com/jcoady/test-kernel',
    keywords='python jupyter ipython kernel',
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python',
                 'Framework :: IPython',
                 'License :: OSI Approved'],
    packages=['testkernel'],
    include_package_data=True,
    install_requires=["test-kernel"],
    cmdclass=cmdclass('testkernel'),
    package_data={'testkernel': ['kernel.json']},

)
