
#ImportModules
import ShareYourSystem as SYS

#define
class ChildrenClass(SYS.TeamerClass):pass

#define
MyTeamer=SYS.TeamerClass(
	).team(
		'Children',
		{
			'MyInt':0
		},
		_ClassesDict={
			'Children':ChildrenClass
		}
	)

#print
print("MyTeamer is ")
SYS._print(MyTeamer)


