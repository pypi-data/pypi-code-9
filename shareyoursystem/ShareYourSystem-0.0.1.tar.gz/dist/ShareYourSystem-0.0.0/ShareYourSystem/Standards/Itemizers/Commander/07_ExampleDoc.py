
#ImportModules
import ShareYourSystem as SYS

#define and command with one get key str
MyCommander=SYS.CommanderClass(
	).get(
		'/ChildCommander/ChildCommander',
	).command(
		'ChildCommander',
		{
			'MyInt':0
		},
		_BeforeWalkRigidBool=True
	)

#print
print('MyCommander is ')
SYS._print(MyCommander)