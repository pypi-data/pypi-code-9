

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
					'LeakingSymbolPrefixStr':'V',
					'-Inputs':{
						'|Rest':{
							'LeakingWeightVariable':'#scalar:-70*mV'
						},
						'|External':{
							'LeakingWeightVariable':'#scalar:15*mV'
						}
					},
					'LeakingNoiseStdVariable':5.,
					'LeakingThresholdVariable':'#scalar:V>-50*mV',
					'LeakingResetVariable':-60.,
					'LeakingAutoCorrelationBool':True
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
			'PyplotingGridVariable':(20,40),
			'-Panels':[
							(
								'|Run',
								{
								}
							),
							(
								'|Stat',
								{
									'PyplotingTextVariable':[-0.6,0.],
									'PyplotingShapeVariable':[5,15],
									'PyplotingShiftVariable':[["top",1],12],
									'-Charts':{
										'|P_Auto':{
												
											}
										}
								}
							)
				]
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



