
#ImportModules
import ShareYourSystem as SYS
from ShareYourSystem.Tutorials import Multiplier

#Definition a Multiplier
MyMultiplier=Multiplier.MultiplierClass().update(
	[
		('MultiplyingFirstInt',2),
		('MultiplyingSecondInt',3)
	]
)

#Definition the AttestedStr
SYS._attest(
	[
		'MyMultiplier is '+SYS._str(
		MyMultiplier,
		**{
			'RepresentingBaseKeyStrsListBool':False,
			'RepresentingAlineaIsBool':False
		}
		)
	]
) 

#Print

