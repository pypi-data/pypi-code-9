
#ImportModules
import ShareYourSystem as SYS

#Define and direct point with an automatic keystr
MyPointer=SYS.PointerClass(
		).point(
			#PointingToGetVariable
			'/ChildPointer/GrandChildPointer'
		)

#print
print('MyPointer is')
SYS._print(MyPointer)

