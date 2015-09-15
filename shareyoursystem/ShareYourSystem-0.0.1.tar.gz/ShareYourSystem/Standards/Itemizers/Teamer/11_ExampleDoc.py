#ImportModules
import ShareYourSystem as SYS

#define structure
MyTeamer=SYS.TeamerClass(
	).get(
		{
			'#key':'-Children',
			'#map@set':{
				'MyStr':"hello"
			}

		}
	)

#print
print('MyTeamer is ')
SYS._print(MyTeamer)

