
#ImportModules
import ShareYourSystem as SYS

#init
MyListDict=SYS.ListDict()

#update
MyListDict.update(
	[
		('MyInt',66),
		('MyDict',{'n':22})
	]
)

#insert
MyListDict.insert(1,'salut')
MyListDict.insert(1,'bonjour','MyStr')

#np
import numpy as np

#set
MyArray=np.array([[1,2]])

#insert
MyListDict.insert(0,MyArray,'MyArray')

#move
MyListDict.move(0,3)

#move
MyListDict.move('MyStr',0)

#print
print('MyListDict is ')
print(MyListDict)
