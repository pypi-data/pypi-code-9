
#ImportModules
import ShareYourSystem as SYS

#Define and map a translation 
MySetter=SYS.SetterClass(
	).set(
		'MyList',
		{
			'#value:#lambda':{
				'MyStr':'#__BonjourStr Erwan #__EndStr'
			},
			'#map':[
				{
					'#__BonjourStr':'Salut',
					'#__EndStr':'!'
				},
				{
					'#__BonjourStr':'Au revoir',
					'#__EndStr':'?'
				}
			]
		}
	)

#print
print('MySetter is ')
SYS._print(MySetter)

#Just one translated word but that is getted
MySetter=SYS.SetterClass(
	).set(
		'HelloStr',
		'Hello'
	).set(
		'ByeStr',
		'Bye'
	).set(
			'MyList',
			{
				'#value:#lambda':{
					'MyStr':'#__Variable Erwan'
				},
				'#map@get':['HelloStr','ByeStr']
			}
		)

#print
print('MySetter is ')
SYS._print(MySetter)

