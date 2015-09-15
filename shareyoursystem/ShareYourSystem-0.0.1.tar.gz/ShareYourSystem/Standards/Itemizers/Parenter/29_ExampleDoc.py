
#ImportModules
import ShareYourSystem as SYS

#array original
MyParenter=SYS.ParenterClass(
	).array(
		[
			['-Connections'],
			['|_^_|E','|_^_|I']
		],
		[
			{},
			{
				'SynapsingBrianKwargVariablesDict':{'pre':'ge+=1.62*mV'},
				'SynapsingProbabilityVariable':0.02
			}
		]
	)

#Definition the AttestedStr
print('MyParenter is ')
SYS._print(MyParenter)

