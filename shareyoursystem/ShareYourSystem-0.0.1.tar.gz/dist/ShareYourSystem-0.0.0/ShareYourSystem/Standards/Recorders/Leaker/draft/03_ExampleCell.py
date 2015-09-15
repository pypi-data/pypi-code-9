#/###################/#
# Import modules
#

#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#Definition an instance
MyLeaker=SYS.LeakerClass(
	).mapSet(
		{
			'LeakingUnitsInt':3,
			'LeakingTimeConstant':20.,
			'-Interactions':{
				'|/':{
				
				}
			}
		}	
	).leak(
	)
	#.simulate(
	#	500.
	#)
	
#/###################/#
# Print
#

#Definition the AttestedStr
print('MyLeaker is ')
SYS._print(MyLeaker) 

#/###################/#
# View
#

"""
#MyLeaker['/-Traces/|*v/-Samples/|Default'].pyplot()
#MyLeaker['/-Events/|Default'].pyplot()
MyLeaker.pyplot()
SYS.matplotlib.pyplot.show()
"""
