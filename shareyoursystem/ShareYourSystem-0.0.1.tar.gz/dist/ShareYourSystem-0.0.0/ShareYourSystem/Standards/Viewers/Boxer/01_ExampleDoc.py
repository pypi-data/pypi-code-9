
#ImportModules
import ShareYourSystem as SYS

#Definition an Tree instance
MyBoxer=SYS.BoxerClass().view()
MyBoxer.MeteoredConcurrentDDPClientVariable.stop()
		
#Definition the AttestedStr
SYS._attest(
	[
		'MyBoxer is '+SYS._str(
		MyBoxer,
		**{
			'RepresentingBaseKeyStrsListBool':False,
			'RepresentingAlineaIsBool':False
		}
		)
	]
)  

#Print

