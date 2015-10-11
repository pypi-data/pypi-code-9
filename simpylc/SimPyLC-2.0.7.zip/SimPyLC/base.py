# ====== Legal notices
#
# Copyright (C) 2013 GEATEC engineering
#
# This program is free software.
# You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicence.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY, without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the QQuickLicence for details.
#
# The QQuickLicense can be accessed at: http://www.geatec.com/qqLicence.html
#
# __________________________________________________________________________
#
#
#  THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!
#
# __________________________________________________________________________
#
# It is meant for training purposes only.
#
# Removing this header ends your licence.
#

import os

_programName = 'SimPyLC'
_programVersion = '2.0.7'
_programNameAndVersion = '{0} {1}'.format (_programName, _programVersion)
_programDir = os.getcwd () .replace ('\\', '/') .rsplit ('/', 3) [-1]

def _getTitle (name):
	return '{0} - {1} - {2}' .format (_programDir, name, _programNameAndVersion)	

def _evaluate (anObject):
	if hasattr (anObject, '__call__'):
		return anObject ()
	else:
		return anObject
			
class _ColorsHex:
	def __init__ (self):
		self.panelBackgroundColor = '#000000'
		
		self.pageCaptionForegroundColor = '#ffffff'
		self.pageCaptionBackgroundColor = self.panelBackgroundColor
		
		self.groupCaptionForegroundColor = '#dddddd'
		self.groupCaptionBackgroundColor = self.panelBackgroundColor
		
		self.labelForegroundColor = '#aaaaaa'
		self.labelBackgroundColor = self.panelBackgroundColor
		
		self.entryReleasedForegroundColor = '#00ff00'
		self.entryReleasedBackgroundColor = '#002200'
		self.entryEditForegroundColor = '#bbbbff'
		self.entryEditBackgroundColor = '#000022'
		self.entryForcedForegroundColor = '#ffaa00'
		self.entryForcedBackgroundColor = '#331100'
		
		self.white = '#ffffff'
		self.silver = '#c0c0c0'
		self.gray = '#808080'
		self.black = '#000000'
		self.red = '#ff0000'
		self.maroon = '#800000'
		self.yellow = '#ffff00'
		self.olive = '#808000'
		self.lime = '#00ff00'
		self.green = '#008000'
		self.aqua = '#00ffff'
		self.teal = '#008080'
		self.blue = '#0000ff'
		self.navy = '#000080'
		self.fuchsia = '#ff00ff'
		self.purple = '#800080'
	
_colorsHex = _ColorsHex ()

for varName in vars (_colorsHex):
	vars () [varName + 'Hex'] = getattr (_colorsHex, varName)
		
for varName in vars (_colorsHex):
	colorHex = getattr (_colorsHex, varName) [1:]
	vars () [varName] = (int (colorHex [0:2], 16) / 255., int (colorHex [2:4], 16) / 255., int (colorHex [4:6], 16) / 255.)
	
def hexFromRgb (rgb):
	rgb = (int (255 * rgb [0]), int (255 * rgb [1]), int (255 * rgb [2]))
	return '#{:02x}{:02x}{:02x}'.format (*rgb)
	
_backgroundColorFactor = 0.25

def backgroundFromRgb (rgb):
	return (_backgroundColorFactor * rgb [0], _backgroundColorFactor * rgb [1], _backgroundColorFactor * rgb [2])
	
def decapitalize (aString):
	return aString [0] .lower () + aString [1:] if aString else ''
	
def underConstruction ():
	print 'THIS SIMULATION IS UNDER CONSTRUCTION'
	raw_input ()
	exit ()

	