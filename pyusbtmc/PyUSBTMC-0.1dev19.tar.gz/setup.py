#!/usr/bin/env python
"""
"""
import os,platform,re

from distutils.core import setup,Extension
try:
   from distutils.command.build_py import build_py_2to3 as build_py #for Python3
except ImportError:
   from distutils.command.build_py import build_py     # for Python2

rev="$Revision: 0.1dev19$"
sysname=platform.system()

setup(name="PyUSBTMC",
      version=rev[11:-1],
      author="Noboru Yamamoto, KEK, JAPAN",
      author_email = "Noboru.YAMAMOTO@kek.jp",
      description ="Python module to control USBTMC/USB488 from python",
      long_description=""" Python module to control USBTMC/USB488 from python.
It requires pyusb module and libusb (or openusb) library to run. 
Although it is still in the development stage, it can read/write data from/to the devices.""",
      platforms="tested on MacOSX10.7",
      url="http://www-acc.kek.jp/EPICS_Gr/products/",
      py_modules=["PyUSBTMC","lsusb","usbids",],
      data_files=[("share/misc",['usb.ids'])]
      )

