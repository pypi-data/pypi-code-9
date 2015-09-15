
#ImportModules
import ShareYourSystem as SYS

#Define and append in a list
MyExecuter=SYS.ExecuterClass(
	).set(
		'execute',
		{
			'#value':'self.MyInt=3'
		}
	)

#print
print('MyExecuter is ')
SYS._print(MyExecuter)	
