#ImportModules
import ShareYourSystem as SYS

#define structure
MyParenter=SYS.ParenterClass(
	).get(
		'-Children'
	)

#print
print("MyParenter['-Children'] is ")
SYS._print(MyParenter['-Children'].ParentDeriveTeamerVariable)


