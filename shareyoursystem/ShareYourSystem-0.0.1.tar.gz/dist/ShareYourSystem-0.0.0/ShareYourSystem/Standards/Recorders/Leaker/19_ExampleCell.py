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
					'LeakingUnitsInt':100,
					'LeakingTransferVariable':'mV*tanh((#CurrentStr)/mV)',
					'-Interactions':{
						'|/':{
							'LeakingWeightVariable':'#array',
							#'LeakingEigenBool':True
						}
					},
					'LeakingGlobalBool':True,
					'RecordingLabelVariable':[0,1,2]
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

#print
print('MyLeaker is ')
SYS._print(MyLeaker) 


