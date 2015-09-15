
#ImportModules
import ShareYourSystem as SYS
from ShareYourSystem.Specials.Simulaters import Populater,Brianer

#Definition of a brian structure
MyBrianer=Brianer.BrianerClass(
	).push(
	[
		(
			'First',
			Populater.PopulaterClass().update(
				[
					('PopulatingUnitsInt',3),
					(
						'PopulatingEquationStr',
						'''
							dv/dt = (10-(v+50))/(20*ms) : volt

						'''
					)
					('MoniteringTrackTuplesList',
						[
							('State','v',[0,1],1.)
						]
					),
					('ConnectingCatchGetStrsList',
						[
							'/NodePointDeriveNoder/<Connectome>SecondRater'
						]
					),
					('ConnectingGraspClueVariablesList',
						[
							'/NodePointDeriveNoder/<Connectome>SecondRater'
						]
					)
				]
			)
		),
		(
			'Second',
			Rater.RaterClass().update(
				[
					('PopulatingUnitsInt',1)
				]
			)
		)
	],
	**{
		'CollectingCollectionStr':'Connectome'
	}
).run(2.)	
		
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

SYS._print(
	MyBrianer.BrianedNeuronGroupsList[0].__dict__
)

#import matplotlib
#plot(MyBrianer['<Connectome>FirstRater'].)

#Print


