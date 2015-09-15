
#ImportModules
import ShareYourSystem as SYS

#Define
OneList=['1',SYS.SetterClass()]

#Define
MySetter=SYS.SetterClass(
	).set(
		'MyList',
		OneList
	)

MySetter.set(
		'#copy:MyCopyList',
		OneList
	)

MySetter.MyList.append(44)
MySetter.MyCopyList.append(55)

#print
print('MySetter is ')
SYS._print(MySetter)

#print
print('OneList is ')
SYS._print(OneList)