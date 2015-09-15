
#ImportModules
import ShareYourSystem as SYS

#Explicit expression
MyPointer=SYS.PointerClass(
		).point(
			'/ChildPather/FirstGrandChildPather',
			'/MyGrandChildPointer/'
		)

#print
print("MyPointeris")
SYS._print(MyPointer)

#print
print("MyPointer['*MyGrandChildPointer'] is")
SYS._print(MyPointer['*MyGrandChildPointer'])

