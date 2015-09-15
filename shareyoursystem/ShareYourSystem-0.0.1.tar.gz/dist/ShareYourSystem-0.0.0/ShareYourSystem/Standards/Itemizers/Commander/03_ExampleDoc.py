
#ImportModules
import ShareYourSystem as SYS

#Init an int
SYS.PatherClass.ShareCountInt=0

#Set
CommandingSetVariable=[
	(
		'execute',
		';'.join(
			[
				'self.ShareCountInt=self.__class__.ShareCountInt',
				'self.__class__.ShareCountInt+=1'
			]
		)
	) for __Int in xrange(2)
]

#define and command
FirstCommander=SYS.CommanderClass(
	)['#map@set'](
			[
				('FirstPather',SYS.PatherClass()),
				('SecondPather',SYS.PatherClass()),
			]
	).command(
		#CommandingGraspVariable,
		[
			'FirstPather','SecondPather'
		],
		#CommandingSetVariable	
		CommandingSetVariable
	)

#print
print('FirstCommander is ')
SYS._print(FirstCommander)

#Init an int
SYS.PatherClass.ShareCountInt=0

#define and command
SecondCommander=SYS.CommanderClass(
	)['#map@set'](
		[
				('FirstPather',SYS.PatherClass()),
				('SecondPather',SYS.PatherClass()),
		]
	).command(
		#CommandingGraspVariable (map or not),
		[
			'FirstPather','SecondPather'
		],
		#CommandingUpdateList	
		CommandingSetVariable,
		#CommandingOrderStr
		"EachSetForAllGets"	
	)

#print
print('SecondCommander is ')
SYS._print(SecondCommander)	

