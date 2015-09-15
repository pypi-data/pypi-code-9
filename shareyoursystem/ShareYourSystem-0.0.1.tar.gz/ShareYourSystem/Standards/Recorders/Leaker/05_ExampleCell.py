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
					'LeakingUnitsInt':2,
					'LeakingSymbolPrefixStr':'r',
					'-Inputs':{
						'|Default':{
							#'LeakingWeightVariable':'#scalar:4.*mV'
							'LeakingWeightVariable':4.
						}
					},
					'-Interactions':{
						'|/':{
							#'LeakingWeightVariable':'#scalar:0.',
							#'LeakingWeightVariable':'#scalar:-1.',
							#'LeakingWeightVariable':-1.,
							'LeakingWeightVariable':[-0.,-0.5,-0.,-0.],
							#'LeakingWeightVariable':[[0.,0.],[0.,-0.4]],
							#'LeakingWeightVariable':'#array',
							#'NumscipyingStdFloat':0.1,
							#'LeakingVariableStr':'I_Default',
							#'BrianingDebugVariable':0.1,
						}
					},
					#'BrianingDebugVariable':0.1,
					'RecordingLabelVariable':[0,1]
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
			'PyplotingGridVariable':(30,20)
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

