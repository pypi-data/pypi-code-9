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
				'|P':{
					'LeakingUnitsInt':2,
					'LeakingSymbolPrefixStr':'V',
					'-Inputs':{
						'|Rest':{
							'LeakingWeightVariable':'#scalar:-60*mV'
						},
						'|External':{
							'LeakingWeightVariable':'#scalar:11*mV'
						}
					},
					'LeakingNoiseStdVariable':0.1,
					'LeakingThresholdVariable':'#scalar:V>-50*mV',
					'LeakingResetVariable':'#scalar:V=-70*mV',
					'-Interactions':{
						'|/':{
							#'BrianingDebugVariable':100,
							'LeakingWeightVariable':[[0.,-1.],[-2.,0.]],
							'LeakingInteractionStr':"Spike",
							#'LeakingDelayVariable':5., #ms
							#'LeakingDelayVariable':[[0.,1.],[5.,0.]], #ms
						}
					},
					'RecordingLabelVariable':[0,1],
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
		200.
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
SYS._print(MyLeaker) 



