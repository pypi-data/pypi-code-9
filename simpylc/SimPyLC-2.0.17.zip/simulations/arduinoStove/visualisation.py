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

from SimPyLC import *

class Visualisation (Scene):
	def __init__ (self):
		Scene.__init__ (self)
		
		self.frame = Beam (size = (2, 2, 0.05), pivot = (0, 1, 0), color = (0.1, 0.1, 0.1))
		self.plate = Cylinder (size = (0.6, 0.6, 0.1), center = (0, 0, 0.05))
		self.buzzer = Cylinder (size = (0.2, 0.2, 0.2), center = (0, 0, 0.05))
		
		self.aDisplay = Beam (size = (1, 2, 0.05), center = (-2, 0, 2), pivot = (0, 1, 0), color = (0.2, 0.2, 0.2))
		self.digit = Beam (size = (0.9, 0.45, 0.05), center = (0, 0, 0.05), color = (0, 0.05, 0))
		self.segment = Beam (size = (0.30, 0.07, 0.05), center = (0, 0, 0.05), color = (0, 1, 0))
		
		self.segments = (
			(0, 2, 3, 4, 5, 6),
			(5, 6),
			(0, 1, 2, 4, 5),
			(0, 1, 2, 5, 6),
			(1, 3, 5, 6),
			(0, 1, 2, 3, 6),
			(0, 1, 2, 3, 4, 6),
			(0, 5, 6),
			(0, 1, 2, 3, 4, 5, 6),
			(0, 1, 2, 3, 5, 6)
		)
		
	def display (self):
		def getPlateColor (temperature):
			return tMul ((1 + temperature) / 10., (1, 0.7, 0))
			
		def getDigit (shift, digitValue):
			def getSegmentColor (segmentNr):
				return (0, 1, 0) if not digitValue == None and segmentNr in self.segments [digitValue ()] else (0, 0.07, 0)
				
			return self.digit (shift = shift, parts = lambda:
				self.segment (angle = 90, shift = (0, 0.4, 0), color = getSegmentColor (0)) +
				self.segment (angle = 90, color = getSegmentColor (1)) +
				self.segment (angle = 90, shift = (0, -0.4, 0), color = getSegmentColor (2)) +
				self.segment (shift = (-0.2, -0.17, 0), color = getSegmentColor (3)) +
				self.segment (shift = (0.2, -0.17, 0), color = getSegmentColor (4)) +
				self.segment (shift = (-0.2, 0.17, 0), color = getSegmentColor (5)) +
				self.segment (shift = (0.2, 0.17, 0), color = getSegmentColor (6))
			)
	
		self.frame (angle = 30, parts = lambda:
			self.plate (shift = (-0.6, -0.6, 0), color = getPlateColor (world.control.plate0Temp)) +
			self.plate (shift = (-0.6, 0.6, 0), color = getPlateColor (world.control.plate1Temp)) +
			self.plate (shift = (0.6, 0.6, 0), color = getPlateColor (world.control.plate2Temp)) +
			self.plate (shift = (0.6, -0.6, 0), color = getPlateColor (world.control.plate3Temp)) +
			self.buzzer (color = (1, 1, 1) if world.control.buzzer else (0.1, 0.1, 0.1))
		)
		self.aDisplay (angle = 70, parts = lambda:
			getDigit ((0, -0.75, 0), world.control.digitValue if world.control.digitIndex == 3 else None) + 
			getDigit ((0, -0.25, 0), world.control.digitValue if world.control.digitIndex == 2 else None) +
			getDigit ((0, 0.25, 0), world.control.digitValue if world.control.digitIndex == 1 else None) +
			getDigit ((0, 0.75, 0), world.control.digitValue if world.control.digitIndex == 0 else None) 
		)
	