#!/usr/bin/env python

""" Distutils Setup File for the eGenix mxODBC Zope DA.

"""
#
# Run web installer, if needed
#
import mxSetup, os
mxSetup.run_web_installer(
    os.path.dirname(os.path.abspath(__file__)),
    landmarks=('Products', 'PREBUILT'))

#
# Load configuration(s)
#
import egenix_mxodbc_zopeda
configurations = (egenix_mxodbc_zopeda,)

#
# Run distutils setup...
#
import mxSetup
mxSetup.run_setup(configurations)
