#!/usr/local/bin/python

""" Configuration for the eGenix mxODBC Zope DA.

    Copyright (c) 2001-2015, eGenix.com Software GmbH; mailto:info@egenix.com
    See the documentation for further information on copyrights,
    or contact the author. All Rights Reserved.
"""
from mxSetup import UnixLibrary, mx_Extension, check_zope_product_version, \
     mx_version, rebase_packages, rebase_files, rebase_extensions
import sys, os

#
# Package version
#
version = mx_version(2, 2, 3,
                     #snapshot=1
                     )

# Make sure that the Zope version file matches this package version:
if (os.path.exists('Products/mxODBCZopeDA/version.txt') and
    not check_zope_product_version(version,
                                   'Products/mxODBCZopeDA/version.txt')):
    sys.stderr.write('WARNING: Zope version.txt mismatch\n')

#
# Setup information
#
name = "egenix-mxodbc-zopeda"

#
# Meta-Data
#
description = "eGenix mxODBC Zope/Plone Database Adapter for Plone 4 and Zope 2"
long_description = """\
eGenix mxODBC Database Adapter for Plone and Zope
-------------------------------------------------

The eGenix mxODBC Database Adaptor for Plone and Zope (mxODBC Zope DA)
allows you to easily connect Plone and Zope to ODBC data sources you
have configured on your system via the Windows ODBC Manager on Windows
or iODBC/unixODBC/DataDirect on Unix platforms.

The adapter is based on our high-performance, reliable and robust
mxODBC Python interface for ODBC compatible databases and supports
ODBC drivers for MS SQL Server and MS Access, Oracle Database, IBM DB2
and Informix, Sybase ASE and Sybase Anywhere, MySQL, PostgreSQL, SAP
MaxDB and many more.

The mxODBC Zope DA package includes everything you need to connect to
ODBC data sources from Plone and Zope. It works with Plone 4.0, 4.1,
4.2 and 4.3, Zope 2.12 and 2.13, supports Python 2.6 and 2.7, and runs
on Windows, Linux, Mac OS X, FreeBSD, Solaris and AIX, in 32- or
64-bit variants.

Downloads
---------

For downloads, documentation, changelog and feature list, please visit
the product page at:

    http://www.egenix.com/products/zope/mxODBCZopeDA/

Licenses
--------

For evaluation and production licenses, please visit our product
page at:

   http://www.egenix.com/products/zope/mxODBCZopeDA/#Licensing

The software is brought to you by eGenix.com and is covered by the
eGenix.com Commercial License 1.3.0.
"""
license = (
"eGenix.com Commercial License 1.3.0; "
"Copyright (c) 2000-2015, eGenix.com Software GmbH, All Rights Reserved."
)
author = "eGenix.com Software GmbH"
author_email = "info@egenix.com"
maintainer = "eGenix.com Software GmbH"
maintainer_email = "info@egenix.com"
url = "http://www.egenix.com/products/zope/mxODBCZopeDA/"
download_url = 'https://downloads.egenix.com/python/download_url/%s/%s/' % (
    name,
    version)
classifiers = [
    "Environment :: Console",
    "Environment :: No Input/Output (Daemon)",
    "Framework :: Plone",
    "Framework :: Plone :: 4.0",
    "Framework :: Plone :: 4.1",
    "Framework :: Plone :: 4.2",
    "Framework :: Plone :: 4.3",
    "Framework :: Plone :: 5.0",
    "Framework :: Zope2",
    "Intended Audience :: Developers",
    "License :: Other/Proprietary License",
    "Natural Language :: English",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX",
    "Operating System :: POSIX :: BSD :: FreeBSD",
    "Operating System :: POSIX :: Linux",
    "Operating System :: Unix",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Other OS",
    "Programming Language :: C",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Topic :: Communications",
    "Topic :: Database",
    "Topic :: Database :: Database Engines/Servers",
    "Topic :: Database :: Front-Ends",
    "Topic :: Documentation",
    "Topic :: Internet",
    "Topic :: Office/Business",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities ",
    ]
if 'a' in version or 'dev' in version:
    classifiers.append("Development Status :: 3 - Alpha")
elif 'b' in version:
    classifiers.append("Development Status :: 4 - Beta")
else:
    classifiers.append("Development Status :: 5 - Production/Stable")
classifiers.sort()

#
# Python packages
#
packages = [
    'Products.mxODBCZopeDA'
    ]

#
# Data files
#
data_files = [

    # User interface
    'Products/mxODBCZopeDA/connection.dtml',
    'Products/mxODBCZopeDA/datasources.dtml',
    'Products/mxODBCZopeDA/addConnection.dtml',
    'Products/mxODBCZopeDA/editConnection.dtml',
    'Products/mxODBCZopeDA/testConnection.dtml',
    'Products/mxODBCZopeDA/testConnectionResults.dtml',
    'Products/mxODBCZopeDA/help.dtml',
    'Products/mxODBCZopeDA/error.html',
    'Products/mxODBCZopeDA/zopeda.css',

    # Documentation
    'Products/mxODBCZopeDA/mxODBC.pdf',
    'Products/mxODBCZopeDA/mxODBCZopeDA.pdf',

    # Special Zope .txt files
    'Products/mxODBCZopeDA/version.txt',
    'Products/mxODBCZopeDA/REFRESH.txt',

    # Standard .txt files
    'Products/mxODBCZopeDA/README.txt',
    'Products/mxODBCZopeDA/COPYRIGHT.txt',
    'Products/mxODBCZopeDA/LICENSE.txt',

    # Icons
    'Products/mxODBCZopeDA/egenix-mxodbc-zopeda-icon.gif',

    ]

#
# C Extension Packages (these extend packages and data_files as needed)
#

# The Zope DA itself does not have any extension modules
ext_modules = []

### Add egenix-mx-base rebased to Products/mxODBCZopeDA/

import egenix_mx_base

packages.extend(
    rebase_packages(egenix_mx_base.packages,
                    new_base_package='Products.mxODBCZopeDA'))

data_files.extend(
    rebase_files(egenix_mx_base.data_files,
                 new_base_dir='Products/mxODBCZopeDA'))

ext_modules.extend(
    rebase_extensions(egenix_mx_base.ext_modules,
                      new_base_package='Products.mxODBCZopeDA',
                      new_base_dir='Products/mxODBCZopeDA'))

### Add egenix-mxodbc rebased to Products/mxODBCZopeDA/

import egenix_mxodbc

packages.extend(
    rebase_packages(egenix_mxodbc.packages,
                    new_base_package='Products.mxODBCZopeDA'))

data_files.extend(
    rebase_files(egenix_mxodbc.data_files,
                 new_base_dir='Products/mxODBCZopeDA'))

ext_modules.extend(
    rebase_extensions(egenix_mxodbc.ext_modules,
                      new_base_package='Products.mxODBCZopeDA',
                      new_base_dir='Products/mxODBCZopeDA'))

# Declare namespace packages (for building eggs)
namespace_packages = [
    'Products',
    ]
      
