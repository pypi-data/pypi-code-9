#ImportModules
import operator
import ShareYourSystem as SYS
import ShareYourSystem as SYS,Binder
from ShareYourSystem.Standards.Objects import Initiator

#Definition a MakerClass decorated by the BinderClass
@Binder.BinderClass(**{
	'ObservingWrapMethodStr':'make',
	'BindingIsBool':True,
	'BindingDecorationMethodStr':'foo',
	'BindingItemTuplesList':[('MyFooInt',1)]
})
class MakerClass(Initiator.InitiatorClass):

	#Definition
	RepresentingKeyStrsList=[
								'MakingMyFloat',
								'MadeMyInt'
							]

	def default_init(self,
					_MakingMyFloat=0.,
					_MadeMyInt=0,
					**_KwarVariablesDict
				):
		pass

	#Definition a Binding function
	def foo(self,*_LiargVariablesList,**_KwarVariablesDict):

		#print
		print('In the foo method ')
		print('_KwarVariablesDict is ')
		print(_KwarVariablesDict)
		print('')

		#get the wrapped method
		WrapUnboundMethod=getattr(
			getattr(
				SYS,
				_KwarVariablesDict['BindDoClassStr']
			),
			_KwarVariablesDict['BindObserveWrapMethodStr']
		)

		#call
		WrapUnboundMethod(self,10.*self.MakingMyFloat)


	def do_make(self):
		
		#Print
		print('I make')
		
		#cast
		self.MadeMyInt=int(self.MakingMyFloat)

#Definition and do a first make
MyMaker=MakerClass().make(3.)

#Use the other binded method that is completely fooooo
MyMaker.foo_make()

#Definition the AttestedStr
SYS._attest(
	[
		'MakerClass.foo is '+str(MakerClass.foo),
		'MakerClass.foo_make is '+str(MakerClass.foo_make),
		'MyMaker is '+SYS._str(
		MyMaker,
		**{
			'RepresentingBaseKeyStrsListBool':False,
			'RepresentingAlineaIsBool':False
		}
		)
	]
) 

#Print



