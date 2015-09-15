
#ImportModules
import ShareYourSystem as SYS

#define
class ChildClass(SYS.TeamerClass):pass

#define
MyManager=SYS.ManagerClass(
	).manage(
		'Child',
		{
			'MyInt':0
		},
		_ClassesDict={
			'Child':ChildClass
		}
	)

#print
print("MyManager is ")
SYS._print(MyManager)


