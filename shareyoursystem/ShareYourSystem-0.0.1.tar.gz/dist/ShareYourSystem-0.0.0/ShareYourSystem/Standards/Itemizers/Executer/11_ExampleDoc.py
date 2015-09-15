
#ImportModules
import ShareYourSystem as SYS

#Just one translated word but that is getted
MyExecuter=SYS.ExecuterClass(
	)['#map@set'](
		[
			(
				'MyList',[1]
			),
			(
				'MyList.extend',
				[
					{
						'#value:#lambda':{
							'MyStr':'#__Variable Erwan'
						},
						'#map':[
							'hello',
							'Salut'
						]
					}
				]
			)
		]
	)

#print
print('MyExecuter is ')
SYS._print(MyExecuter)
