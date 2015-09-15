
#ImportModules
import ShareYourSystem as SYS

#Explicit expression
MyPointer=SYS.PointerClass(
		).point(
			#PointingToGetVariable
			'/ChildPointer/GrandChildPointer',
			#PointingToSetKeyVariable
			'GrandFamilyPointer/'
		)

#print
print('MyPointer is')
SYS._print(MyPointer)

