#ImportModules
import ShareYourSystem as SYS

#Define
@SYS.PropertiserClass()
class MakerClass(SYS.PrinterClass):

	def default_init(self,
			_MakingMyFloat={
							'DefaultValueType':property,
							'PropertyInitVariable':3.,
							'PropertyDocStr':'I am doing the thing here'
							}	
		):
		SYS.PrinterClass.__init__(self)

#Print and show that the class has already propertize_(get,set,del)MakingMyFloat 
# a default _MakingMyFloat value and the MakingMyFloat prop
print('SYS.MakerClass.__dict__ is')
print(SYS.indent(SYS.MakerClass.__dict__))

#Define
MyMaker=SYS.MakerClass()

#print the __dict__, there is no things related to the 
#MakingMyFloat property
print('MyMaker.__dict__ before set is ')
SYS._print(MyMaker.__dict__)

#set
MyMaker.MakingMyFloat=7.

#print the __dict__, now there is the hidden attribute
print('MyMaker.__dict__ after set is ')
SYS._print(MyMaker.__dict__)

#Define
MyMaker=SYS.MakerClass()

#print the repr : the instance just show the MakingMyFloat key 
#that is actually the get of _MakingMyFloat in the class
print('MyMaker before set is ')
SYS._print(MyMaker)

#set
MyMaker.MakingMyFloat=7.

#print the repr : now the instance shows the _MakingMyFloat
#value that is particulat for the instance
print('MyMaker after set is ')
SYS._print(MyMaker)