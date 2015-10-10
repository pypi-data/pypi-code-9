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

class TrafficLights (Module):
	def __init__ (self):
		Module.__init__ (self)	
		
		self.page ('Trafic lights')
		
		self.group ('Timers', True)
		self.sequenceTimer = Timer ()
		self.tBlink = Register (0.5)
		self.blinkTimer = Timer ()
		
		self.group ('Lights')
		self.redNorth = Marker ()
		self.greenNorth = Marker ()
		self.redSouth = Marker ()
		self.greenSouth = Marker ()
		self.redEast = Marker ()
		self.greenEast = Marker ()
		self.redWest = Marker ()
		self.greenWest = Marker ()
		
		self.group ('Mode switching')
		self.button = Marker ()
		self.buttonPulse = Oneshot ()
		self.modeStep = Register ()
		self.regularMode = Marker (True)
		self.cycleMode = Marker ()
		self.nightMode = Marker ()
		self.offMode = Marker ()
			
		self.group ('Regular phases', True)
		self.northSouthGreen = Marker (True)
		self.northSouthBlink = Marker ()
		self.eastWestGreen = Marker ()
		self.eastWestBlink = Marker ()
		
		self.group ('Cycle phases')
		self.northGreen = Marker ()
		self.northBlink = Marker ()
		self.eastGreen = Marker ()
		self.eastBlink = Marker ()
		self.southGreen = Marker ()
		self.southBlink = Marker ()
		self.westGreen = Marker ()
		self.westBlink = Marker ()
		
		self.group ('Regular times', True)
		self.tNorthSouthGreen = Register (5)
		self.tNorthSouthBlink = Register (7)
		self.tEastWestGreen = Register (12)
		self.tEastWestBlink = Register (14)
		
		self.group ('Cycle times')
		self.tNorthGreen = Register (5)
		self.tNorthBlink = Register (7)
		self.tEastGreen = Register (12)
		self.tEastBlink = Register (14)
		self.tSouthGreen = Register (19)
		self.tSouthBlink = Register (21)
		self.tWestGreen = Register (26)
		self.tWestBlink = Register (28)

		self.group ('System')
		self.runner = Runner ()
			
	def sweep (self):
		self.part ('Timers')
		self.sequenceTimer.reset ((self.regularMode and self.sequenceTimer > self.tEastWestBlink) or (self.cycleMode and self.sequenceTimer > self.tWestBlink))
		self.blinkTimer.reset (self.tBlink)
		
		self.part ('Mode switching')
		self.buttonPulse.trigger (self.button)
		self.modeStep.set ((self.modeStep + 1) % 4, self.buttonPulse)
		self.regularMode.mark (self.modeStep == 0)
		self.cycleMode.mark (self.modeStep == 1)
		self.nightMode.mark (self.modeStep == 2)
		self.offMode.mark (self.modeStep == 3)
		