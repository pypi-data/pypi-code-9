
#ImportModules
import ShareYourSystem as SYS

#Definition a "graph" structure
MyMuziker=SYS.MuzikerClass()
		
#Definition the AttestedStr
SYS._attest(
	[
		'MyMuziker is '+SYS._str(
		MyMuziker,
		**{
			'RepresentingBaseKeyStrsListBool':False,
			'RepresentingAlineaIsBool':False
			}
		)
	]
) 

#Print

