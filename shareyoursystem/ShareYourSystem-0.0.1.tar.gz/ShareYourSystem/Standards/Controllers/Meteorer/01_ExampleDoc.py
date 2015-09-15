
#ImportModules
import ShareYourSystem as SYS

#Definition an Tree instance
MyMeteorer=SYS.MeteorerClass().meteor()
SYS.MeteoredConcurrentDDPClientVariable.stop()
		
#Definition the AttestedStr
SYS._attest(
	[
		'MyMeteorer is '+SYS._str(
		MyMeteorer,
		**{
			'RepresentingBaseKeyStrsListBool':False,
			'RepresentingAlineaIsBool':False
		}
		)
	]
)  

#Print

