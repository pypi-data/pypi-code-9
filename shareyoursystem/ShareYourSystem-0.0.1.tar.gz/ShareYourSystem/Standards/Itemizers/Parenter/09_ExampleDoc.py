
#ImportModules
import ShareYourSystem as SYS

#define structure
MyParenter=SYS.ParenterClass(
	).get(
		'/-Children/|Erwan/-GrandChildren',
		
	).parentDown(
	)

#print
print('MyParenter is ')
SYS._print(MyParenter)

#define structure
MyParenter=SYS.ParenterClass(
	).get(
		'/-Children/|Erwan/-GrandChildren',
		
	)['/-Children/|Erwan/-GrandChildren'].parentUp(
	)

#print
print('MyParenter is ')
SYS._print(MyParenter)
