#ImportModules
import ShareYourSystem as SYS

#Define and manage without specifying the value class 
#which is PointerClass if Teamer not imported else TeamerClass
MyManager=SYS.ManagerClass(
	).manage(
		#ManagingKeyStr
		'First'
	)

#Define and manage with specifying the Variable
MyManager.manage(
		#ManagingKeyStr
		'Second',
		#ManagingValueVariable
		SYS.TeamerClass()
	)

#Set with a setitem access and the symbolic shortcut
MyManager['|Third']=SYS.TeamerClass()

#direct get
print('MyManager.ThirdTeamer is ')
print(MyManager.ThirdTeamer)

#Print
print('MyManager is ')
SYS._print(MyManager)

#We can have all the ManagementDict with the symbolic shortcut get
print("MyManager['|'] is ")
SYS._print(MyManager['|'])

#We can have all the ManagementDict with the symbolic shortcut get
print("MyManager['|.values'] is ")
SYS._print(MyManager['|.values'])

