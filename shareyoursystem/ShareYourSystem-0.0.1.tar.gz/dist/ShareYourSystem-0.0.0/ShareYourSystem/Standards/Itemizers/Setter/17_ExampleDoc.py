
#ImportModules
import ShareYourSystem as SYS

#Define
MySetter=SYS.SetterClass(
	).get(
		{
			'#key':'ChildSetter',
			'#set':('MyInt',0)
		}
	)

#print
print('MySetter is ')
SYS._print(MySetter)
