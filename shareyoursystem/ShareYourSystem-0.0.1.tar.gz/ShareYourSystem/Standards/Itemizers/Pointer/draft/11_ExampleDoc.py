
#ImportModules
import ShareYourSystem as SYS

#Define and shortcut point without SetKeyVariable
MyPointer=SYS.PointerClass(
		).get(
			'->/ChildPointer/FirstGrandChildPointer'
		).get(
			'<->/ChildPointer/SecondGrandChildPointer'
		)

#print
print('MyPointer is')
SYS._print(MyPointer)

