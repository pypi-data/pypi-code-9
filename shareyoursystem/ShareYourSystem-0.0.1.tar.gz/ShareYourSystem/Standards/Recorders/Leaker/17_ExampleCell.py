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
					#'LeakingThresholdVariable':'#scalar:V>-50*mV',
					'LeakingThresholdVariable':-50.,
					'LeakingResetVariable':'#scalar:V=-70*mV',
					'-Interactions':{
						'|/':{
							#'BrianingDebugVariable':100,
							'LeakingWeightVariable':[[0.,0.],[0.,0.]],
							'LeakingInteractionStr':"Spike",
							'LeakingPlasticRuleVariable':"J-=(((V_post+60.*mV)/mV)+((1.+0.)/2.)*J)*(int(i!=j))",
							#'LeakingPlasticRuleVariable':"J-=0.5*J",
							'RecordingLabelVariable':[0,1,2,3]
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
		500.
	)

#/###################/#
# View
#

MyLeaker.mapSet(
		{
			'PyplotingGridVariable':(20,20)
		}
	).mapSet(
		{
			'-Panels':{
				'|Run':{
					'-Charts':{
						'|P_/_J':{
							'PyplotingLegendDict':{
									'fontsize':10,
									'ncol':2
								}
							}
					}
				}
			}

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


