
#ImportModules
import ShareYourSystem as SYS
from ShareYourSystem.Specials.Simulaters import Populater,Brianer

#Definition
MyBrianer=Brianer.BrianerClass(
	).update(
		{
			#Set here the global net parameters
			'StimulatingStepTimeFloat':0.1
		}
	).produce(
		['E','I'],
		Populater.PopulaterClass,
		{
			#Here are defined the brian classic shared arguments between pops
			'brian.NeuronGroupInspectDict':SYS.InspectDict().update(
				{
					'LiargVariablesList':[
						0,
						'''
							dv/dt = (ge+gi-(v+49*mV))/(20*ms) : volt
							dge/dt = -ge/(5*ms) : volt
							dgi/dt = -gi/(10*ms) : volt
						'''
					],
					'KwargVariablesDict':
					{
						'threshold':'v>-50*mV'
						'reset':'v=-60*mV'
					}
				}
			),
			#Here are the settig of future brian monitors
			'push':
			{
				'LiargVariablesList':
				[
					[
						Moniter.MoniterClass.update(
								{
									'brian.SpikeMonitorInspectDict':SYS.InspectDict()
								}
							)
					],
				],
				'KwargVariablesDict':{'CollectingCollectionStr':'Monitome'}
			},
			#Init conditions
			'PopulatingInitDict':
			{
				'v':-60.
			}
		},
		**{'CollectingCollectionStr':'Populatome'}
	).__setitem__(
		'Dis_<Populatome>',
		#Here are defined the brian classic specific arguments for each pop
		[
			{
				'Exec_NeuronGroupInspectDict["LiargVariablesList"][0]':3200,
				'ConnectingGraspClueVariablesList':
				[
					SYS.GraspDictClass(
						{
							'HintVariable':'/NodePointDeriveNoder/<Populatome>IPopulater',
							'SynapseArgumentVariable':
							{
								'pre':'ge+=1.62*mV'
								'connect':{'p':0.02}
							}
						}
					)
				]
			},
			{
				'Exec_NeuronGroupInspectDict["LiargVariablesList"][0]':800,
				'ConnectingGraspClueVariablesList':
				[
					SYS.GraspDictClass(
						{
							'HintVariable':'/NodePointDeriveNoder/<Populatome>EPopulater',
							'SynapseArgumentVariable':
							{
								'pre':'gi-=9*mV'
								'connect':{'p':0.02}
							}
						}
					)
				]
			}
		]
	).brian()
		
#Definition the AttestedStr
SYS._attest(
	[
		'MyBrianer is '+SYS._str(
		MyBrianer,
		**{
			'RepresentingBaseKeyStrsList':False,
			'RepresentingAlineaIsBool':False
		}
		),
	]
) 

#SYS._print(MyBrianer.BrianedMonitorsList[0].__dict__)

#SYS._print(
#	MyBrianer.BrianedNeuronGroupsList[0].__dict__
#)

#import matplotlib
#plot(MyBrianer['<Connectome>FirstRater'].)

#Print


