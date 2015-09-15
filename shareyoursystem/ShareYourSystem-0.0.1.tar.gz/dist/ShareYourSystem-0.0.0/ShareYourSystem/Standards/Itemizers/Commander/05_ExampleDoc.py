
#ImportModules
import ShareYourSystem as SYS


#define and command with one get key str
MyCommander=SYS.CommanderClass(
	).command(
		#CommandingGetVariable
		'/',
		#CommandingSetVariable
		{
			'MyStr':"hello"	
		}		
	)

#print
print('MyCommander.GettedValueVariable is ')
print(MyCommander.GettedValueVariable)

#command with just one variable
SYS.CommanderClass.printHello=lambda _SelfVariable:SYS._print(
	_SelfVariable.MyStr
)
MyCommander.command('/','#call:printHello')
