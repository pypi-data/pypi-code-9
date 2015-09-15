
#ImportModules
import ShareYourSystem as SYS

#Define and shortcut point with SetKeyVariable
MyPointer=SYS.PointerClass(
		).set(
			'->/ChildPointer/GrandChildPointer',
			'MyGrandChildPointer'
		).set(
			'->/ChildPointer/SecondGrandChildPointer',
			'/MySecondGrandChildPointer/'
		)

#print
print('MyPointer is')
SYS._print(MyPointer)

