
#ImportModules
import ShareYourSystem as SYS

#array original
MyConnecter=SYS.ConnecterClass(
	).set(
		'-Neurons',
		{
			'|E':{
				'array':[
					[
						['-Connectomes'],
						['|Posts'],
						['-Connections'],
						['|/^/|E','|/^/|I']
					],
					[
						{},
						{},
						{},
						{
							'MyStr':"hello"
						}
					]
				]
			},
			'|I':{}
		}
	).get('?v')

#print
print('MyConnecter is ')
SYS._print(MyConnecter)


