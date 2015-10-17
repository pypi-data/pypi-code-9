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

class Control (Module):
	def __init__ (self):
		Module.__init__ (self)
		
		self.page ('Four plate stove control with cooking alarm')
		
		self.group ('General buttons', True)
		self.powerButton = Marker ()
		self.powerEdge = Oneshot ()
		self.power = Marker ()
		
		self.group ()
		self.childLockButton = Marker ()
		self.childLockEdge = Oneshot ()
		self.childLock = Marker ()
		self.unlocked = Marker ()
		
		self.group ('Plate selection')
		self.plateSelectButton = Marker ()
		self.plateSelectEdge = Oneshot ()
		self.plateSelectDelta = Register ()
		self.plateSelectNr = Register ()
		self.tempDelta = Register ()
		self.tempChange = Marker ()
		
		self.group ('Up/down buttons')
		self.upButton = Marker ()
		self.upEdge = Oneshot ()
		self.group ()
		self.downButton = Marker ()
		self.downEdge = Oneshot ()
		
		self.group ('Cooking plates', True)
		self.plate0Temp = Register ()
		self.plate0Selected = Marker ()
		
		self.group ()
		self.plate1Temp = Register ()
		self.plate1Selected = Marker ()
		
		self.group ()
		self.plate2Temp = Register ()
		self.plate2Selected = Marker ()
		
		self.group ()
		self.plate3Temp = Register ()
		self.plate3Selected = Marker ()
		
		self.group ('Alarm selection button')
		self.alarmSelectButton = Marker ()
		self.alarmTime = Register ()
		self.alarmTimer = Timer ()
		self.alarmEdge = Oneshot ()
		self.alarmTimeLeft = Register ()
		self.alarmChange = Marker ()
		self.alarmButtonTimer = Timer ()
		self.alarmButtonStep = Register ()
		self.alarmDelta = Register ()
		
		self.group ('Numerical displays', True)
		self.digitIndex = Register ()
		self.plateDigitValue = Register ()
		self.alarmDigitValue = Register ()
		self.digitValue = Register ()
				
		self.group ('Buzzer')
		self.buzzerOnTime = Register (4)
		self.buzzerOnTimer = Timer ()
		self.buzzerOn = Marker ()
		self.buzzerBaseFreq = Register (500.)
		self.buzzerPitchTimer = Timer ()
		self.buzzerFreq = Register ()
		self.buzzerWaveTimer = Timer ()
		self.buzzerEdge = Oneshot ()
		self.buzzer = Marker ()
				
		self.group ('System')
		self.sweepMin = Register (1000)
		self.sweepMax = Register ()
		self.sweepWatch = Timer ()
		self.run = Runner ()
			
	def sweep (self):
		self.part ('Edge triggering of buttons')
		self.powerEdge.trigger (self.powerButton)
		self.power.mark (not self.power, self.powerEdge)
		
		self.childLockEdge.trigger (self.power and self.childLockButton)
		self.childLock.mark (not self.childLock, self.childLockEdge)
		self.unlocked.mark (self.power and not self.childLock)
		
		self.plateSelectEdge.trigger (self.unlocked and self.plateSelectButton)
		self.plateSelectDelta.set (1, self.plateSelectEdge, 0)
		self.plateSelectNr.set ((self.plateSelectNr + self.plateSelectDelta) % 4, self.power, 0)

		self.upEdge.trigger (self.unlocked and self.upButton)
		self.downEdge.trigger (self.unlocked and self.downButton)
				
		self.part ('Cooking alarm')
		self.alarmChange.mark (self.alarmSelectButton and (self.upButton or self.downButton))
		self.alarmButtonTimer.reset (not self.alarmChange)
		self.alarmButtonStep.set (1, self.alarmChange, 0)
		self.alarmButtonStep.set (10, self.alarmButtonTimer > 10)  
		self.alarmButtonStep.set (100, self.alarmButtonTimer > 20)
		self.alarmDelta.set (-self.alarmButtonStep, self.downButton, self.alarmButtonStep)
		self.alarmTime.set (0, self.power and self.upButton and self.downButton, limit (self.alarmTime + self.alarmDelta * world.period, 0, 9999))
		self.alarmEdge.trigger (self.alarmTimer > self.alarmTime)
		self.alarmTimer.reset (self.alarmChange)
		self.alarmTimeLeft.set (max ((self.alarmTime - self.alarmTimer), 0))
		
		self.part ('Cooking plates')
		self.plate0Selected.mark (self.plateSelectNr == 0)
		self.plate1Selected.mark (self.plateSelectNr == 1)
		self.plate2Selected.mark (self.plateSelectNr == 2)
		self.plate3Selected.mark (self.plateSelectNr == 3)
		
		self.tempChange.mark (not self.alarmSelectButton and (self.upEdge or self.downEdge))
		self.tempDelta.set (-1, not self.alarmSelectButton and self.downButton, 1)
		
		self.plate0Temp.set (limit (self.plate0Temp + self.tempDelta, 0, 9), self.tempChange and self.plate0Selected)
		self.plate1Temp.set (limit (self.plate1Temp + self.tempDelta, 0, 9), self.tempChange and self.plate1Selected)
		self.plate2Temp.set (limit (self.plate2Temp + self.tempDelta, 0, 9), self.tempChange and self.plate2Selected)
		self.plate3Temp.set (limit (self.plate3Temp + self.tempDelta, 0, 9), self.tempChange and self.plate3Selected)
		
		self.part ('Buzzer tone generation and pitch bend')
		self.buzzerOnTimer.reset (self.alarmEdge)
		self.buzzerOn.mark (self.buzzerOnTimer < self.buzzerOnTime)
		self.buzzerPitchTimer.reset (self.buzzerPitchTimer > 1)
		self.buzzerFreq.set (self.buzzerBaseFreq * (1 + self.buzzerPitchTimer))
		self.buzzerWaveTimer.reset (self.buzzerWaveTimer > 0.5 / self.buzzerFreq)
		self.buzzerEdge.trigger (self.buzzerWaveTimer == 0)
		self.buzzer.mark (not self.buzzer, self.buzzerOn and self.buzzerEdge)
		
		self.part ('Numerical display')
		self.digitIndex.set ((self.digitIndex + 1) % 4)

		self.plateDigitValue.set (self.plate0Temp, self.digitIndex == 3)
		self.plateDigitValue.set (self.plate1Temp, self.digitIndex == 2)
		self.plateDigitValue.set (self.plate2Temp, self.digitIndex == 1)
		self.plateDigitValue.set (self.plate3Temp, self.digitIndex == 0)
		
		self.alarmDigitValue.set (digit (self.alarmTimeLeft, self.digitIndex))
		self.digitValue.set (self.alarmDigitValue, self.alarmSelectButton, self.plateDigitValue)
		
		self.part ('Sweep time measurement')
		self.sweepMin.set (world.period, world.period < self.sweepMin)
		self.sweepMax.set (world.period, world.period > self.sweepMax)
		self.sweepWatch.reset (self.sweepWatch > 2)
		self.sweepMin.set (1000, not self.sweepWatch)
		self.sweepMax.set (0, not self.sweepWatch)
