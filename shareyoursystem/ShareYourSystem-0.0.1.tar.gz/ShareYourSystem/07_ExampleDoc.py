
#ImportModules
import ShareYourSystem as SYS

#Init
MySetList=SYS.SetList()

#print
print('MySetList is ')
print(MySetList)

#Init
MySetList=SYS.SetList(
	('MyInt',4)
)

#print
print('MySetList is ')
print(MySetList)

#Init
MySetList=SYS.SetList(
	[
		('MyStr',"hello"),
		('MyInt',0)
	]
)

#print
print('MySetList is ')
print(MySetList)

#Init
MySetList=SYS.SetList(
	{
		'MyFloat':5.,
		'MyBool':False
	}
)

#print
print('MySetList is ')
print(MySetList)

#Init
MySetList=SYS.SetList(
	'MyStr'
)

#print
print('MySetList is ')
print(MySetList)





