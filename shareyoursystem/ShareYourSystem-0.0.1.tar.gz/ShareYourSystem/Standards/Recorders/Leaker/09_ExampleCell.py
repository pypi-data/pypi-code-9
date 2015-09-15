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
					'LeakingUnitsInt':3,
					'LeakingSymbolPrefixStr':'V',
					'-Inputs':{
						'|Rest':{
							'LeakingWeightVariable':'#scalar:-60*mV'
						},
						'|External':{
							'LeakingWeightVariable':'#scalar:11*mV'
						}
					},
					'LeakingThresholdVariable':'#scalar:V>-50*mV',
					#'LeakingThresholdVariable':[-55.,-52.5],
					#'LeakingThresholdVariable':{
					#	'MethodsList':[
					#		SYS.Leaker.detectThreshold
					#	],
					#	'ThresholdVariable':[-55.,-52.5,-50.]
					#},
					'LeakingResetVariable':'#scalar:V=-70*mV',
					'BrianingMonitorIndexIntsList':[0,1,2],
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

#print
print('MyLeaker is ')
SYS._print(MyLeaker) 


