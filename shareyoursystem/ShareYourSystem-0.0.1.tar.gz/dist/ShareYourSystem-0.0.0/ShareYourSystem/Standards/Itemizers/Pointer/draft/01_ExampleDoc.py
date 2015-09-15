
#ImportModules
import ShareYourSystem as SYS


#Point direct with a special Key str
MyPointer=SYS.PointerClass().point(
			#PointingToGetVariable
			'/ChildPointer/GrandChildPointer',
			#PointingToSetKeyVariable
			'MyGrandChildPointer'
		)

#print
print('MyPointer is')
SYS._print(MyPointer)



