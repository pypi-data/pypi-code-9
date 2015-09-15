#ImportModules
import ShareYourSystem as SYS
import operator

#Definition a MakerClass decorated by the ObserverClass
@SYS.ObserverClass(**{
	'ObservingIsBool':True,
	'ObservingWrapMethodStr':'make'
})
class MakerClass(object):

	def default_init(self,
					_MakingMyFloat=0.,
					_MadeMyInt=0,
					**_KwarVariablesDict
				):
		object.__init__(self,**_KwarVariablesDict)

	def do_make(self):
		
		#cast
		self.MadeMyInt=int(self.MakingMyFloat)

#Definition the AttestedStr
SYS._attest(
	[
		'MakerClass.make is '+str(MakerClass.make),
		'MakerClass.DeriveClassor.ObservingWrapMethodStr is '+str(
			MakerClass.DeriveClassor.ObservingWrapMethodStr),
		'MakerClass.DeriveClassor.ObservedWrapMethodStr is '+str(
			MakerClass.DeriveClassor.ObservedWrapMethodStr),
	]
) 

#Print



