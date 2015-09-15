#ImportModules
import ShareYourSystem as SYS

#Represent a dict
Dict={
	'ParentDict':
		{
		'ChildDict':
			{
				'MyInt':0
			},
		'MyStr':'hello'
		}
	}

#Represent a TuplesList
TuplesList=[
				(
					'ParentTuplesList',
					[
						(
							'ChildDict',
							{
								'MyInt':0
							}
						)
					]
				),
				('MyStr','hello')
			]

#Definition the AttestedStr
print('Dict is'+SYS._str(Dict))
print('TuplesList is'+SYS._str(TuplesList))

