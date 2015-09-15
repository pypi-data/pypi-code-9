
#ImportModules
import ShareYourSystem as SYS

#Explicit expression
MyPointer=SYS.PointerClass(
		).point(
			#PointingToGetVariable
			'/FirstChildPointer/GrandChildPointer',
			#PointingToSetKeyVariable
			'MyGrandChildPointer',
			#PointingBackBool
			_BackBool=True
		)

#print
print('MyPointer is')
SYS._print(MyPointer)

