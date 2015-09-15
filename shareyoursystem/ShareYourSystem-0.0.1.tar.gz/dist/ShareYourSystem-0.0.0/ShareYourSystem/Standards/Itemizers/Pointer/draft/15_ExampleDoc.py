
#ImportModules
import ShareYourSystem as SYS

#Define and shortcut back point with SetKeyVariable
MyPointer=SYS.PointerClass(
		).set(
			'<->/ChildPointer/FirstGrandChildPointer',
			('MyFirstGrandChildPointer','MyGrandParentPointer')
		).set(
			'<->/ChildPointer/SecondGrandChildPointer',
			('/MySecondGrandChildPointer/','/MyGrandParentPointer/')
		)

#print
print('MyPointer is')
SYS._print(MyPointer)
