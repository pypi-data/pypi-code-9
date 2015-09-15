#ImportModules
import ShareYourSystem as SYS

#Definition a MakerClass decorated by the DefaultorClass
@SYS.DoerClass()
class MakerClass(object):

	def default_init(self,
				_MakingMyFloat=1.,
				_MakingShareList=['bonjour'],
				_MakingSpecificList=None,
				_MakingMyInt={'DefaultValueType':int}
				):
		object.__init__(self)


#print at the class level
print("\n".join(
	[
		'MakerClass has some special attributes',
		'MakerClass.DoingAttributeVariablesOrderedDict is '+SYS.indent(
			MakerClass.DoingAttributeVariablesOrderedDict),
		'MakerClass.DoneAttributeVariablesOrderedDict is '+SYS.indent(
			MakerClass.DoneAttributeVariablesOrderedDict)
	])
)

#Definition a default instance
DefaultMaker=MakerClass()

#print
print(
	'\n'+'\n'.join(
		[
			'What are you saying DefaultMaker ?',
			'DefaultMaker.__dict__ is '+SYS.indent(DefaultMaker.__dict__),
			'DefaultMaker.getDo() is '+SYS.indent(DefaultMaker.getDo()),
		]
	)
)

#Definition a special instance
SpecialMaker=MakerClass(
	_MakingSpecificList=['hello'],
	**{
		'MakingMyFloat':3.
	}
)

#print
print(
	'\n'+'\n'.join(
		[
			'What are you saying SpecialMaker ?',
			'SpecialMaker.__dict__ is '+SYS.indent(SpecialMaker.__dict__),
			'SpecialMaker.getDo() is '+SYS.indent(SpecialMaker.getDo())
		]
	)
)





