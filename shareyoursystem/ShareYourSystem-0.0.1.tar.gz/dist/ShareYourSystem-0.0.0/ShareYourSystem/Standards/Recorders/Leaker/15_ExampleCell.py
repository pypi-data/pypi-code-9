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
			'BrianingStepTimeFloat':0.01,
			'-Populations':{
				'|P':{
					'LeakingUnitsInt':2,
					'LeakingSymbolPrefixStr':'r',
					'-Interactions':{
						'|/':{
							#'BrianingDebugVariable':10,
							'LeakingWeightVariable':[[0.,-20.],[1.,0.]],
							'LeakingDelayVariable':5.,
							#'LeakingDelayVariable':[[2.,1.],0.5], #PRE-POST matrix
							#'LeakingDelayPrepostBool':True,
							#'LeakingDelayVariable':[[0.5,5.],[0.2,1.]],
							#'LeakingDelayCustomBool':True
							'LeakingRecordBool':True
						}
					},
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
		10.
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

#print
print('MyLeaker is ')
SYS._print(MyLeaker['/-Panels/|Run/-Charts'])


