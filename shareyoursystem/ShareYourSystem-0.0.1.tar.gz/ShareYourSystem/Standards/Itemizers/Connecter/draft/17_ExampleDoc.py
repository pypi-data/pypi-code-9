
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
						['-Connections'],
						['|#direct:_^_|E','|#direct:_^_|I']
					],
					[
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


