#ImportModules
import ShareYourSystem as SYS

#Init
MyGetList=SYS.GetList()

#print
print('MyGetList is ')
print(MyGetList)

#Init
MyGetList=SYS.GetList(
	#ListVariable
	'MyInt',
	#GetterVariable
	{'MyInt':4}
)

#print
print('MyGetList is ')
print(MyGetList)

#Init
MyGetList=SYS.GetList([0,2],['hello','bonjour','allo'])

#print
print('MyGetList is ')
print(MyGetList)

#Init
MyGetList=SYS.GetList(['rrr',3])

#print
print('MyGetList is ')
print(MyGetList)

#Init
MyGetList=SYS.GetList(['GetterClass'],SYS)

#print
print('MyGetList is ')
print(MyGetList)

#Init
MyGetList=SYS.GetList('GetterClass',SYS)

#print
print('MyGetList is ')
print(MyGetList)

#Init
MyGetList=SYS.GetList(None,SYS)

#print
print('MyGetList is ')
print(MyGetList)

#Init
MyGetList=SYS.GetList([
		{'GetSortInt':3},
		{'GetSortInt':1}
	])

#print
print('MyGetList is ')
print(MyGetList)




