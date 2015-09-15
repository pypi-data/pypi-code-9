#ImportModules
import ShareYourSystem as SYS

#Definition a MakerClass decorated by the DefaultorClass
@SYS.DoerClass()
class MakerClass(object):

	def default_init(self,
				_MakingMyFloat=1.,
				_MakingShareList=['bonjour'],
				_MakingRestrictList=None,
				_MakingMyInt={'DefaultValueType':int}
				):
		object.__init__(self)

	def do_make(self):

		#print
		print('Maker : I am going to make')
		print('')

		#set
		self.MadeMyInt=int(self.MakingMyFloat)
	
#print
print('InspectMethodDict is ')
print(SYS.indent(MakerClass.InspectMethodDict))

#print
print("\n".join([
	'MakerClass.do_make is '+str(MakerClass.do_make),
	'MakerClass.doWithmake is '+str(MakerClass.superDo_make),
	'MakerClass.make is '+str(MakerClass.make),
	'MakerClass.callDo is '+str(MakerClass.callDo),
]))


