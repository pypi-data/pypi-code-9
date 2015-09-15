
#ImportModules
import ShareYourSystem as SYS

#Define
MyConditioner=SYS.ConditionerClass(
	)

MyConditioner.mapGet(
		[
			'MyList',
			'MyInt',
			'YourStr'
		]
	)

MyConditioner.ConditioningDirectBool=True

ConditionList=MyConditioner.mapCondition(
		[
			[
				(SYS.startswith,'My')
			],
			[
				(SYS.endswith,'YourStr')
			]
		],
		MyConditioner.__dict__.keys(),
		_DirectBool=True
	)

#print
print('ConditionList is')
SYS._print(ConditionList)

