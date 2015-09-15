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
				'set':{
					'#liarg:#lambda':{
						'|#NeuronStr':{
							'BrianingRecordSkipKeyStrsList':['ge','gi'],
							'#copy:BrianingNeurongroupDict':{
								'N':'#UnitsInt',
								'model':
								'''
									dv/dt = (-(v+60*mV)+11*mV + ge + gi+ 0.1*mV*sqrt(20.*ms)*xi)/(20*ms) : volt
									dge/dt = -ge/(5*ms) : volt
									dgi/dt = -gi/(10*ms) : volt
								''',
								'threshold':'v>-50*mV',
								'reset':'v=-70*mV'
							},
							'set':{
								'#liarg:#lambda':{
									'array':[
										[
											['-Projectomes'],
											['|Default'],
											['-Projections'],
											[
												'|/^/|E',
												'|/^/|I'
											]
										],
										[
											{},
											{},
											{},
											{
												'BrianingSynapsesDict':{
													'pre':'''
														#PreStr \n
													'''
												},
												'BrianingConnectVariable':0.2
											}
										]
									]
								},
								'#map':[
									['#PreStr'],
									[
										['ge+=0.1*mV'],
										['gi-=3*mV']
									]
								]
							},
							'-Traces':{
								'|v':{
									'NumscipyingStdFloat':0.001,
									'-Samples':{
										'|Default':{
											'RecordingLabelVariable':[0,1]
										}
									}
								}
							},
							'-Events':{
								'|Default_Events':{
								}
							},
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
			'PyplotingGridVariable':[30,20]
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

