#ImportModules
import ShareYourSystem as SYS
import numpy as np

#Define
@SYS.DoerClass()
class MakerClass(object):

	def default_init(self,
				_MakingMyFloat=1.,
				_MakingMyArray=None,
				_MakingMyList=None,
				_MakingFirstInt={'DefaultValueType':int},
				_MakingSecondInt=0,
				_MakingThirdInt=1,
				_MadeMyInt=0,
				_MadeMyList=None,
				):
		object.__init__(self)

	def do_make(self):

		#print
		print('Maker : I am going to make')
		print('self.MakingMyFloat is ',self.MakingMyFloat)
		print('')

		#set
		self.MadeMyInt=int(self.MakingMyFloat)
	
#Look at the decorated make method
AttestingStrsList=['MakerClass.make is '+str(MakerClass.make)]

#Definition of an instance and make
MyMaker=MakerClass(
		_MakingMyList=['hello'],
		**{'MakingFirstInt':3}
	).superDo_make(
		3.,
		np.array([5]),
		_SecondInt=5,
		**{'MakingThirdInt':6}
	)

#Add
print("\n".join([
		'After the make ',
		'MyMaker.MakingMyFloat is '+str(MyMaker.MakingMyFloat),
		#Special numpy variables also...check Doer l 431 to compare them to None...
		'MyMaker.MakingMyArray is '+str(MyMaker.MakingMyArray),
		'MyMaker.MakingMyList is '+str(MyMaker.MakingMyList),
		'MyMaker.MakingFirstInt is '+str(MyMaker.MakingFirstInt),
		'MyMaker.MakingSecondInt is '+str(MyMaker.MakingSecondInt),
		'MyMaker.MakingThirdInt is '+str(MyMaker.MakingThirdInt),
		'MyMaker.MadeMyInt is '+str(MyMaker.MadeMyInt),
		'MyMaker.MadeMyList is '+str(MyMaker.MadeMyList)
	]
))

