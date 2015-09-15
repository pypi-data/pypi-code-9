
#ImportModules
import ShareYourSystem as SYS

#Definition and update with an exec Str
MyExecuter=SYS.ExecuterClass()
MyExecuter.MyList=[1]

#print a get
print("MyExecuter['>>self.__dict__.keys()'] is ")
SYS._print(MyExecuter['>>self.__dict__.keys()'])

#print a set 
MyExecuter['MyStr']=">>'I belong to the '+str(self.__class__.MroClassesList[0])"

#also a quick shortcut for call method of the getted object
MyExecuter['MyList.append']=[3]

#also a quick shortcut for call method of the getted object
MyExecuter['MyList.append']=[4]

#also a quick shortcut for call method of the getted object
MyExecuter['MyList.pop']

#print
print('MyExecuter is ')
SYS._print(MyExecuter)