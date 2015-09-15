#ImportModules
import ShareYourSystem as SYS

#define structure
MyTeamer=SYS.TeamerClass(
	).team(
		'Things',
		{
			'MyInt':0,
			'MyStr':"hello"
		},
		_WrapBool=False
	).set(
		'-#direct:Stuffs',
		{
			'MyBool':False
		}
	)	

#print
print('MyTeamer is ')
SYS._print(MyTeamer)

