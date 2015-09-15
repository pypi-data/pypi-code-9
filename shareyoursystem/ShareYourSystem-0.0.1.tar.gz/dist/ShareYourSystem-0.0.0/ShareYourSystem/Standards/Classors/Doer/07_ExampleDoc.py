#ImportModules
import ShareYourSystem as SYS

#Define
@SYS.DoerClass()
class MakerClass(object):

	def default_init(self,
				_MakingMyFloat=0.,
				_MadeShareClassor=SYS.ClassorClass(),
				_MadeSpecificClassor=None
				):
		object.__init__(self)

	def do_make(self):

		#print
		print('Maker : I am going to make... but I do nothing')
		print('')

	
#Definition of an instance and make
MakerClass.MadeShareClassor.MyInt=5
MyMaker=MakerClass(
	).make(
		3.
	)

#Add
print("\n".join([
		'After the make ',
		'MakerClass.MadeSpecificClassor is '+str(MakerClass.MadeSpecificClassor),
		'MyMaker.MadeShareClassor.__dict__ is '+str(MyMaker.MadeShareClassor.__dict__),
		'MyMaker.MadeSpecificClassor is '+str(MyMaker.MadeSpecificClassor)
	]))


