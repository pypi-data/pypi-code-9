
#ImportModules
import ShareYourSystem as SYS
from ShareYourSystem.Tutorials import Sumer

#Definition a Sumer
MySumer=Sumer.SumerClass().update(
	[
		('SumingFirstInt',2),
		('SumingSecondInt',3)
	]
)

#Definition the AttestedStr
SYS._attest(
	[
		'MySumer is '+SYS._str(
		MySumer,
		**{
			'RepresentingBaseKeyStrsListBool':False,
			'RepresentingAlineaIsBool':False
		}
		)
	]
) 

#Print

