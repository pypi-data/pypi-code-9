#ImportModules
import ShareYourSystem as SYS

#define structure
MyManager=SYS.ManagerClass(
	).manage(
		'Thing',
		{
			'MyInt':0,
			'MyStr':"hello"
		},
		_WrapBool=False
	).set(
		'|#direct:Stuff',
		{
			'MyBool':False
		}
	)	

#print
print('MyManager is ')
SYS._print(MyManager)

