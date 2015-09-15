
#ImportModules
import ShareYourSystem as SYS

#define and team
MyManager=SYS.ManagerClass(
	).set(
		'|Thing',
		{
			'MyInt':0
		}
	)

#print
print('MyManager is ')
SYS._print(MyManager)


