
#ImportModules
import ShareYourSystem as SYS

#array original
MyPointer=SYS.PointerClass(
	).set(
		'-Neurons',
		{
			'|E':{
				'array':[
					[
						['-Connections'],
						['|Postlets<->Prelets'],
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
print('MyPointer is ')
SYS._print(MyPointer)


