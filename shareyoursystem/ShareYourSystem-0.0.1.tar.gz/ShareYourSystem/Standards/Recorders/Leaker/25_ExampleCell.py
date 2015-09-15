

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
					'LeakingSymbolPrefixStr':'r',
					'-Inputs':{
						'|External':{
							'LeakingWeightVariable':'#custom:#clock:100*ms:1.*mV*(t==100.*ms)'
						}
					},
					'-Interactions':{
						'|/':{
							'LeakingWeightVariable':[
								[1.5,-2.6],
								[3.1,-0.9]
							]
						}
					},
					'LeakingMaxBool':True,
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
		300.
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

#print(MyLeaker['-Panels'])
#print(MyLeaker['/-Populations/|P/-Traces'].ManagementDict.keys())

#/###################/#
# Print
#

#print
print('MyLeaker is ')
SYS._print(MyLeaker) 



