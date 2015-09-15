#ImportModules
import ShareYourSystem as SYS

#Define
@SYS.PropertiserClass()
class MakerClass(object):

	def default_init(self,
			_MakingMyList=None,
			_MakingMyInt={
							'DefaultValueType':property,
							'PropertyInitVariable':None,
							'PropertyDocStr':'I am doing the thing here',
							'ShapeDict':{
								'MakingMyList':0
							}
						},
			_MadeMyInt=0	
		):
		object.__init__(self)


#Define
MyMaker=MakerClass()

#Set and this will bind the value of MakingMyInt 
MyMaker.MakingMyInt=2

#print
print('MyMaker.__dict__ is ')
print(SYS.indent(MyMaker))

