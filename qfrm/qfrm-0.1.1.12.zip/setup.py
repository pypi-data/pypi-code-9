from setuptools import setup, find_packages

setup(
name='qfrm',
version='0.1.1.12',      # MAJOR.MINOR[.PATCH[.sub]], http://semver.org/
description='Quantitative Financial Risk Management: awesome OOP tools for measuring, managing and visualizing risk of financial instruments and portfolios.',
#long_description=open('README.txt').read(),   # ReST source for PyPI QFRM package home page
url='http://oleg.rice.edu/stat-449-649-fall-2015/',
author='Oleg Melnikov',
author_email='xisreal@gmail.com',
maintainer='Oleg Melnikov',
maintainer_email='xisreal@gmail.com',
license='LICENSE.txt',
packages=find_packages(exclude=['', '', '']),       # ['qfrm'],
zip_safe=False,
keywords='finance risk management bond duration yield curve duration',
classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Financial and Insurance Industry',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Topic :: Office/Business :: Financial',
    'Topic :: Office/Business :: Financial :: Investment',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Utilities',
    'License :: OSI Approved :: GNU General Public License (GPL)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
],
    # Core modules: time, math, numbers
install_requires=[
    'pandas >= 0.16.2','numpy >= 1.9.2','scipy >= 0.16.0','matplotlib >= 1.4.3','statistics',
],
)

# TODO:
# keyword, examples, platforms

#---  Some helpful packaging manuals and tutorials
# http://docs.python.org/3.4/distutils/
# http://packaging.python.org/en/latest/
# http://pythonhosted.org/setuptools/setuptools.html
# http://the-hitchhikers-guide-to-packaging.readthedocs.org/en/latest
# http://thomas-cokelaer.info/tutorials/sphinx/docstring_python.html
# http://pymotw.com/2/doctest
# http://epydoc.sourceforge.net/fields.html
# http://peterdowns.com/posts/first-time-with-pypi.html
# http://pythonwheels.com/

# http://docutils.sourceforge.net/docs/user/rst/quickref.html#external-hyperlink-targets

#--- Prepare for distribution (creates qfrm*.zip file and uploads to PyPI, if registered earlier)
# python setup.py register
# python setup.py sdist
# python setup.py sdist -n # dry run
# python setup.py sdist upload
# python setup.py bdist_wheel
# python setup.py sdist
# python setup.py sdist bdist_wininst upload

