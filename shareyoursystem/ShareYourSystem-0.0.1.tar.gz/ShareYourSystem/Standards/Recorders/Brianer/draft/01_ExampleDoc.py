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
					'NeurongroupingBrianKwargDict':
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
							'get':'>>self.NeurongroupingBrianKwargDict[\'N\']=#UnitsInt',
						}
					},
					'#map':[
						['#NeuronStr','#UnitsInt'],
						[
							['E','3200'],
							['I','800']
						]
					]
				}
			)
		]
	).network(
		['Populations']
	).brian()

#print
print('MyBrianer is ')
SYS._print(MyBrianer) 


print(
	MyBrianer['/-Populations/|E'].NeurongroupedBrianVariable.equations._equations.keys()
)


"""
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
MyBrianer.simulate(300)

#plot
ME=MyBrianer['/-Populations/|E/-Spikes/|Run'].SpikeMonitor
MI=MyBrianer['/-Populations/|I/-Spikes/|Run'].SpikeMonitor
from matplotlib import pyplot
pyplot.plot(ME.t/brian2.ms, ME.i, 'r.')
pyplot.plot(MI.t/brian2.ms, ME.source.N+MI.i, 'b.')
pyplot.show()
"""
