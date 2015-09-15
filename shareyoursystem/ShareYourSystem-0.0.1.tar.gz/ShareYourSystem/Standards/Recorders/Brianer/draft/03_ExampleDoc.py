#ImportModules
import ShareYourSystem as SYS

#Definition
MyBrianer=SYS.BrianerClass(
	).set(
		'-Populations',
		[
			(
				'ManagingBeforeSetVariable',
				{
					'NeurongroupingBrianKwargVariablesDict':
					{
						'model':
						'''
							dv/dt = (ge+gi-(v+49*mV))/(20*ms) : volt
							dge/dt = -ge/(5*ms) : volt
							dgi/dt = -gi/(10*ms) : volt
						''',
						'threshold':'v>-50*mV',
						'reset':'v=-60*mV'
					},
					'get':'/-Spikes/|Run',
				}
			),
			(
				'set',
				{
					'#liarg:#lambda':{
						'|#NeuronStr':{
							'SimulatingUnitsInt':3200,
							'array':[
								[
									['-<->'],
									['|Postlets<->Prelets'],
									['|#direct:_^_|E','|#direct:_^_|I']
								],
								[
									{},
									{},
									{
										'SynapsingBrianKwargVariablesDict':{'pre':'#PreStr'},
										'SynapsingProbabilityVariable':0.02
									}
								]
							]
						}
					},
					'#map':[
						['#NeuronStr','#PreStr'],
						[
							['E','ge+=1.62*mV'],
							['I','gi-=9*mV']
						]
					]
				}
			)
		]
	).network(
		['Populations']
	)

#print
print('MyBrianer is ')
SYS._print(MyBrianer) 


"""
	.brian(
	)



#init
import brian2
map(
	lambda __BrianedNeuronGroup:
	__BrianedNeuronGroup.__setattr__(
		'v',
		-60*brian2.mV
	),
	MyBrianer.BrianedNeuronGroupsList
)

#run
MyBrianer.run(300)

#plot
ME=MyBrianer['/-Populations/|E/-Spikes/|Run'].SpikeMonitor
MI=MyBrianer['/-Populations/|I/-Spikes/|Run'].SpikeMonitor
from matplotlib import pyplot
pyplot.plot(ME.t/brian2.ms, ME.i, 'r.')
pyplot.plot(MI.t/brian2.ms, ME.source.N+MI.i, 'b.')
pyplot.show()
"""
