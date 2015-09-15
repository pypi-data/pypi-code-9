#ImportModules
import ShareYourSystem as SYS

#Define a Unbound method like function
def foo(_InstanceVariable,*_LiargVariablesList,**_KwargVariablesDict):

	#print
	print('In the foo function ')
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
	WrapUnboundMethod(_InstanceVariable,10.*_InstanceVariable.MakingMyFloat)


#Definition a MakerClass decorated by the BinderClass
@SYS.BinderClass(**{
	'ObservingWrapMethodStr':'make',
	'BindingIsBool':True,
	'BindingDecorationUnboundMethod':foo,
	'BindingItemTuplesList':[('MyFooInt',1)]
})
class MakerClass(object):

	def default_init(self,
					_MakingMyFloat=0.,
					_MadeMyInt=0,
					**_KwarVariablesDict
				):
		object.__init__(self)

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








