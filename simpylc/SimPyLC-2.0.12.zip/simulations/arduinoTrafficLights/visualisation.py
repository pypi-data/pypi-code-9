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

class TrafficLamp (Cylinder):
	def __init__ (self, green = False):
		Cylinder.__init__ (self, size = (0.1, 0.1, 0.2), center = (0, 0, 0.5) if green else (0, 0, 0.7), color = (0, 1, 0) if green else (1, 0, 0))
		self.originalColor = self.color

	def __call__ (self, on):
		self.color = self.originalColor if on else tMul (0.2, self.originalColor)
		return Cylinder.__call__ (self)

class StreetLamp (Cylinder):
	def __init__ (self, green = False):
		Cylinder.__init__ (self, size = (0.4, 0.4, 0.4), center = (0, 0, 2), color = (1, 1, 0.2))
		self.originalColor = self.color

	def __call__ (self, brightness):
		self.color = tMul (0.2 + 0.8 * brightness, self.originalColor)
		return Cylinder.__call__ (self)

class Visualisation (Scene):
	def __init__ (self):
		Scene.__init__ (self)
		
		self.crossing = Beam (size = (3, 3, 0.1), pivot = (0, 1, 0), color = (0, 0.3, 0))
		self.leg = Beam (size = (1.5, 1.5, 0.1), center = (0.75, 0, 0.1), joint = (-0.75, 0, 0), color = (0.1, 0.1, 0.1))	
		self.pole = Cylinder (size = (0.05, 0.05, 1), center = (0.7, 0.775, 0.45), color = (1, 1, 1))
		
		red = (1, 0, 0)
		green = (0, 1, 0)

		self.redLamp = TrafficLamp ()
		self.greenLamp = TrafficLamp (True)
		self.streetLamp = StreetLamp ()		
		
	def display (self):
		control = world.trafficLights
		
		self.crossing (30, lambda:
			self.leg (0, lambda:
				self.pole (lambda:
					self.redLamp (control.northRedLamp) +
					self.greenLamp (control.northGreenLamp)
				)
			) +
			self.leg (-90, lambda:
				self.pole (lambda:
					self.redLamp (control.eastRedLamp) +
					self.greenLamp (control.eastGreenLamp)
				)
		
			) +
			self.leg (-180, lambda:
				self.pole (lambda:
					self.redLamp (control.southRedLamp) +
					self.greenLamp (control.southGreenLamp)
				)
			) +
			self.leg (-270, lambda:
				self.pole (lambda:
					self.redLamp (control.westRedLamp) +
					self.greenLamp (control.westGreenLamp)
				)
			) +
			self.streetLamp ((control.streetLamp - control.brightMin) / (control.brightMax - control.brightMin))
		)
	