
#ImportModules
import ShareYourSystem as SYS

#Define and append in a list
MyExecuter=SYS.ExecuterClass(
	).get(
		'MyList'
	).set(
		'MyDict.__setitem__',
		{
			'#value:#map@get':['#direct:MyCloneList','MyList']
		}
	)

#print
print('MyExecuter is ')
SYS._print(MyExecuter)	
