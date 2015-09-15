#ImportModules
import ShareYourSystem as SYS

#Define
@SYS.DoerClass()
class MakerClass(SYS.PrinterClass):

	def default_init(self,
						_MakingMyFloat=0.,  
						_MadeMyInt=0
					):
		SYS.PrinterClass.__init__(self)

#Define
MyMaker=MakerClass()
YourMaker=MakerClass()

#print normally
print(MyMaker.__repr__())

#print and remove one specific default 
MyMaker.PrintingClassSkipKeyStrsList.append('MadeMyInt')
print(MyMaker.__repr__())
print(YourMaker.__repr__())

#print and remove one specific default 
MyMaker.PrintingClassForceKeyStrsList.append('Module')
print(MyMaker.__repr__())
print(YourMaker.__repr__())

#print and remove one specific default 
MyMaker.PrintingInstanceForceKeyStrsList.append('NameStr')
print(MyMaker.__repr__())
print(YourMaker.__repr__())