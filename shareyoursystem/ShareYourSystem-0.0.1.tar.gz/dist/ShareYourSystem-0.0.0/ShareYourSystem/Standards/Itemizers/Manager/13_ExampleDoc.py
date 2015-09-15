
#ImportModules
import ShareYourSystem as SYS

#define
MyManager=SYS.ManagerClass(
	).manage(
		'Child',
		{
			'MyInt':0
		},
		_AfterSetVariable={
			'MyStr':"hello"
		}
	)

#print
print("MyManager is ")
SYS._print(MyManager)


