
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
						['-Interactomes'],
						['|Posts'],
						['-Interactions'],
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
	)

#mapConnect
MyConnecter['/-Neurons/|E/'].mapConnect('Interact')

#print
print('MyConnecter is ')
SYS._print(MyConnecter)


