#ImportModules
import ShareYourSystem as SYS

#Definition a MakerClass decorated by the BinderClass
@SYS.BinderClass(**{
	'ObservingWrapMethodStr':'make',
	'BindingIsBool':True,
	'BindingDecorationMethodStr':'foo',
	'BindingItemTuplesList':[('MyFooInt',1)]
})
class MakerClass(object):

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
		object.__init__(self)

	#Definition a Binding function
	def foo(self,*_LiargVariablesList,**_KwargVariablesDict):

		#print
		print('In the foo method ')
		print('_KwargVariablesDict is ')
		print(_KwargVariablesDict)
		print('')

		#get the wrapped method
		WrapUnboundMethod=getattr(
			getattr(
				SYS,
				_KwargVariablesDict['BindDoClassStr']
			),
			_KwargVariablesDict['BindObserveWrapMethodStr']
		)

		#call
		WrapUnboundMethod(self,10.*self.MakingMyFloat)


	def do_make(self):
		
		#Print
		print('I make')
		
		#cast
		self.MadeMyInt=int(self.MakingMyFloat)

#print
print('Do first a make')

#Definition and do a first make
MyMaker=MakerClass().make(3.)

#print
print('do a foo_make')

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



