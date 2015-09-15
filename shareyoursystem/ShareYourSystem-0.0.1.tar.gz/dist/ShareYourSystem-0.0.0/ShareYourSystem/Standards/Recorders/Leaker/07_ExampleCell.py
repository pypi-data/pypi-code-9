#/###################/#
# Import modules
#

#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#Define
MyLeaker=SYS.LeakerClass(
	).mapSet(
		{
			'-Populations':{
				'|Default':{
					'LeakingUnitsInt':1,
					'LeakingSymbolPrefixStr':'r',
					'-Inputs':{
						'|Default':{
							'LeakingWeightVariable':5.
						}
					},
					'-Interactions':{
						'|/':{
							'LeakingWeightVariable':-1.,
						}
					},
					'LeakingTransferVariable':'1.*mV*tanh((#CurrentStr)/(1.*mV))',
					#'LeakingTransferVariable':lambda __Float:__Float,
					#'BrianingDebugVariable':100
				}
			}
		}
	).leak(
	)

#/###################/#
# Do one simulation
#

MyLeaker.simulate(
		500.
	)

#/###################/#
# View
#

MyLeaker.mapSet(
		{
			'PyplotingGridVariable':(20,20)
		}
	).view(
	).pyplot(
	).show(
	)

#/###################/#
# Print
#

#Definition the AttestedStr
print('MyLeaker is ')
SYS._print(MyLeaker) 


