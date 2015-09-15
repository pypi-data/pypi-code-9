
#ImportModules
import ShareYourSystem as SYS

#Define and append in a list
MyExecuter=SYS.ExecuterClass(
	).get(
		'MyList'
	).set(
		'MyList.append',
		[6]
	).set(
		'MyList.append',
		{
			'#value:#get':'>>self.MyList.__getitem__(0)'
		}
	)

#print
print('MyExecuter is ')
SYS._print(MyExecuter)	
