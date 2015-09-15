
#ImportModules
import ShareYourSystem as SYS

#Definition an Tree instance
MyViewer=SYS.ViewerClass().view()
MyViewer.MeteoredConcurrentDDPClientVariable.stop()
		
#Definition the AttestedStr
SYS._attest(
	[
		'MyViewer is '+SYS._str(
		MyViewer,
		**{
			'RepresentingBaseKeyStrsListBool':False,
			'RepresentingAlineaIsBool':False
		}
		)
	]
)  

#Print

