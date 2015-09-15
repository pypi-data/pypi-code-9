#ImportModules
import ShareYourSystem as SYS

#Define
@SYS.PropertiserClass()
class MakerClass(object):

	def default_init(self,
			_MakingMyList={
							'DefaultValueType':property,
							'PropertyInitVariable':None,
							'PropertyDocStr':'I am doing the thing here',
							'ShapeKeyStrsList':['MakingMyInt']
							},
			_MakingMyInt=3,
			_MadeMyInt=0	
		):
		object.__init__(self)


#Define
MyMaker=MakerClass()

#Set and this will bind the value of MakingMyInt 
MyMaker.MakingMyList=[3,4]

#print
print('MyMaker.__dict__ is ')
print(SYS.indent(MyMaker))
print(MyMaker.__class__.DefaultAttributeVariablesOrderedDict['MakingMyList'])

