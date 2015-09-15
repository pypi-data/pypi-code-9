
#ImportModules
import ShareYourSystem as SYS

#define and 
MyManager=SYS.ManagerClass(
	).get(
		'/|First/-Employees/|Designer'
	)

#print
print('MyManager is ')
SYS._print(MyManager)

