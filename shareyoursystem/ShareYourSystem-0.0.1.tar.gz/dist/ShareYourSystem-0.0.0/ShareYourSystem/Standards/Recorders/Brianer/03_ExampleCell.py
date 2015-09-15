#/###################/#
# Import modules
#

#ImportModules
import ShareYourSystem as SYS

#/###################/#
# Build the model
#

#Definition an instance
MyBrianer=SYS.BrianerClass(
	).mapSet(
		{
			'-Populations':
			{
				'ManagingBeforeSetVariable':{
					'#copy:BrianingNeurongroupDict':{
						'model':
						'''
							dv/dt = (-(v+60*mV)+11*mV + 5.*mV*sqrt(20.*ms)*xi)/(20*ms) : volt
						''',
						'threshold':'v>-50*mV',
						'reset':'v=-70*mV'
					},
					'-Traces':{
						'|v':{
							'NumscipyingStdFloat':0.001
						}
					},
					'-Events':{
						'|Default_Events':{
						}
					}
				},
				'set':{
					'#liarg:#lambda':{
						'|#NeuronStr':{
							'get':'>>self.BrianingNeurongroupDict[\'N\']=#UnitsInt',
						}
					},
					'#map':[
						['#NeuronStr','#UnitsInt'],
						[
							['E','80'],
							['I','20']
						]
					]
				}
			}
		}	
	).brian(
	)
	
#/###################/#
# Do one simulation
#

MyBrianer.simulate(
		500.
	)

#/###################/#
# View
#

MyBrianer.mapSet(
		{
			'PyplotingGridVariable':[35,20]
		}
	).view(
	).pyplot(
	).show(
	)

#/###################/#
# Print
#

#Definition the AttestedStr
print('MyBrianer is ')
SYS._print(MyBrianer) 
