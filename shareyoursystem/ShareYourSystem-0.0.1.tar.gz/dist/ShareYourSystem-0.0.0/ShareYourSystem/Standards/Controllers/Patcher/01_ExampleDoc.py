
#ImportModules
import ShareYourSystem as SYS

#Definition an Tree instance
MyPatcher=SYS.PatcherClass().produce(
		'Components',
		['A','B'],
		SYS.PatcherClass
	).__setitem__(
		'<Components>APatcher/<Components>aPatcher',
		SYS.PatcherClass()
	).patch()
		
#Definition the AttestedStr
SYS._attest(
	[
		'MyPatcher is '+SYS._str(
		MyPatcher,
		**{
			'RepresentingBaseKeyStrsListBool':False,
			'RepresentingAlineaIsBool':False
		}
		)
	]
)  

#Print

