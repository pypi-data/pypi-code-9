#import SYS
import ShareYourSystem as SYS

#Definition
MyBrianer=SYS.BrianerClass(
	).collect(
		"Neurongroupers",
		'P',
		SYS.NeurongrouperClass(
			#Here are defined the brian classic shared arguments for each pop
			**{
				'NeurongroupingKwargVariablesDict':
				{
					'N':2,
					'model':
					'''
						Jr : 1
						dr/dt = (-r+Jr)/(20*ms) : 1
					'''
				},
				'ConnectingGraspClueVariablesList':
				[
					SYS.GraspDictClass(
						{
							'HintVariable':'/NodePointDeriveNoder/<Neurongroupers>PNeurongrouper',
							'SynapsingKwargVariablesDict':
							{
								'model':
								'''
									J : 1
									Jr_post=J*r_pre : 1 (summed)
								'''
							},
							'SynapsingWeigthSymbolStr':'J',
							'SynapsingWeigthFloatsArray':SYS.array(
								[
									[0.,-2.],
									[4.,0.]
								]
							),
							"SynapsingDelayDict":{'r':1.*SYS.brian2.ms}
						}
					)
				]		
			}
		).collect(
			"StateMoniters",
			'Rate',
			SYS.MoniterClass(
				**{
					'MoniteringVariableStr':'r',
					'MoniteringRecordTimeIndexIntsArray':[0,1]
					}
				)
		)
	).network(
			**{
				'RecruitingConcludeConditionVariable':[
					(
						'MroClassesList',
						SYS.contains,
						SYS.NeurongrouperClass
					)
				]
			}
	).brian()

#init variables
map(
	lambda __BrianedNeuronGroup:
	__BrianedNeuronGroup.__setattr__(
		'r',
		1.+SYS.array(map(float,xrange(__BrianedNeuronGroup.N)))
	),
	MyBrianer.BrianedNeuronGroupsList
)

#run
MyBrianer.run(100)

#plot
M=MyBrianer['<Neurongroupers>PNeurongrouper']['<StateMoniters>RateMoniter'].StateMonitor
SYS.plot(M.t, M.r.T)
SYS.show()
