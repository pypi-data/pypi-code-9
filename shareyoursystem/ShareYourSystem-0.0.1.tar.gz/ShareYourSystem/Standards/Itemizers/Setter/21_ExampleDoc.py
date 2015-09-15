
#ImportModules
import ShareYourSystem as SYS

#Definition a MakerClass
@SYS.ClasserClass(**{
		'ClassingSwitchMethodStrsList':['make']
	}
)
class MakerClass(SYS.SetterClass):

	def default_init(self,
			_MakingMyFloat=0.,
			_MadeMyInt=0	
		):
		SYS.SetterClass.__init__(self)

	def do_make(self):

		#cast
		self.MadeMyInt=(int)(self.MakingMyFloat)


#define and set
MyMaker=MakerClass(
	).make(
		3.
	).make(
		5.
	)

#print
print('MyMaker before switch is ')
SYS._print(MyMaker)

#switch
MyMaker['#map@set'](
		[
			('setSwitch',['make',MakerClass]),
			('setDoing',MakerClass),
		]
	)

#print
print('MyMaker after switch and reset is ')
SYS._print(MyMaker)

#make
MyMaker.make(
		7.
	)

#print
print('MyMaker after swith is ')
SYS._print(MyMaker)




