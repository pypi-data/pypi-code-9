
#ImportModules
import ShareYourSystem as SYS

#Definition a permuter
MyPermuter=SYS.PermuterClass().permute(3,7)

#Definition the AttestedStr
SYS._attest(
	[
		'MyPermuter is '+SYS._str(
		MyPermuter,
		**{
			'RepresentingBaseKeyStrsListBool':False,
			'RepresentingAlineaIsBool':False
		}
		)
	]
) 

#Print

