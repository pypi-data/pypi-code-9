
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
						['|/^/|E','|/^/|I']
					],
					[
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


print(MyConnecter['/-Neurons/|E'].mapConnect('Connect'))


#print
print('MyConnecter is ')
SYS._print(MyConnecter)


#Ioannidis
#Craig Bennett Neural correlates... Salmon thing
