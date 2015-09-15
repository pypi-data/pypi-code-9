
#ImportModules
import ShareYourSystem as SYS

#Definition a Pooler
MyPooler=SYS.PoolerClass().pool(7,12)

#Definition the AttestedStr
SYS._attest(
	[
		'MyPooler is '+SYS._str(
		MyPooler,
		**{
			'RepresentingBaseKeyStrsListBool':False,
			'RepresentingAlineaIsBool':False
		}
		)]
) 

#Print
