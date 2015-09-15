
#ImportModules
import ShareYourSystem as SYS

#Define and map a translation 
MySetter=SYS.SetterClass(
	).set(
		'set',
		{
			'#liarg:#lambda':{
				'My#__KeyStrStr':'#__StartStr Erwan #__EndStr'
			},
			'#map':[
				{
					'#__KeyStr':'French',
					'#__StartStr':'Salut',
					'#__EndStr':'!'
				},
				{
					'#__KeyStr':'English',
					'#__StartStr':'Hello',
					'#__EndStr':'?'
				}
			]
		}
	)

#print
print('MySetter is ')
SYS._print(MySetter)

#Define and map a translation 
MySetter=SYS.SetterClass(
	).set(
		'set',
		{
			'#liarg:#lambda':{
				'My#__KeyStrStr':'#__StartStr Erwan #__EndStr'
			},
			'#map':[
				['#__KeyStr','#__StartStr','#__EndStr'],
				[
					['French','Salut','!'],
					['English','Hello','?']
				]
			]
		}
	)


#print
print('MySetter is ')
SYS._print(MySetter)

