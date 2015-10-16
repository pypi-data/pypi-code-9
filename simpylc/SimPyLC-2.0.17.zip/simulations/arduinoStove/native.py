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

class Native (Code):
	def __init__ (self):
		Code.__init__ (self)
	
	def get (self):
		underConstruction ()
		return '''	
void setup () {
	pinMode (0, INPUT);
	pinMode (1, INPUT);
	pinMode (2, INPUT);
	pinMode (4, INPUT);
	pinMode (7, INPUT);
	pinMode (8, INPUT);
	
	pinMode (3, OUTPUT);
	pinMode (5, OUTPUT);
	pinMode (6, OUTPUT);
	pinMode (9, OUTPUT);
}

void loop () {
	digitalRead (0, powerButton);
	digitalRead (1, childLockButton);
	digitalRead (2, plateSelectButton);
	digitalRead (4, upButton);
	digitalRead (7, downButton);
	digitalRead (8, alarmSelectButton);
	
	analogWrite

	cycle ();

	digitalWrite (31, buzzer);
}
		''' 
