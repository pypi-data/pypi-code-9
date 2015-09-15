
#ImportModules
import ShareYourSystem as SYS

#Define and set a simple Int
MySetter=SYS.SetterClass(
	).set(
		'MyInt',
		0
	)

#we can set ... a set
MySetter.set(
		'set',
		('MyStr',"hello")
	)

MySetter.set(
		'set',
		{
			'#liarg':['MyOtherStr'],
			'#kwarg':{'SettingValueVariable':"bonjour"}
		}
	)

#Note that we can call also a direct explicit function
MySetter.get(
		'MyList'
	)
MySetter.set(
		MySetter.MyList.append,
		#This is the LiargVariablesList version
		[3]
	)
MySetter.set(
		MySetter.MyList.append,
		#If it is just one value it s gonna read as [78]
		78
	)

#print
print('MySetter is ')
SYS._print(MySetter)

#We can call a bound method and the value of the set is the Liarg
MySetter.set(
		'get',
		'MyInt'
	)
	
#print
print('MySetter.GettedValueVariable is ')
SYS._print(MySetter.GettedValueVariable)
