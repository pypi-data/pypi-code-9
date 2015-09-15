#ImportModules
from ShareYourSystem.Standards.Classors import Attester
from ShareYourSystem.Standards.Objects import Hdformater

#Definition a Hdformater that writes an empty hdf file
MyHdformater=Hdformater.HdformaterClass().hdformat().hdfview().hdfclose()
#.hdfview().hdfclose()

#Definition the AttestedStr
SYS._attest(
					[
						'MyHdformater.HdformatedConsoleStr is '+str(
							MyHdformater.HdformatedConsoleStr)
					]
				) 

#Print




#import os
#os.popen('import os;os.popen('')')