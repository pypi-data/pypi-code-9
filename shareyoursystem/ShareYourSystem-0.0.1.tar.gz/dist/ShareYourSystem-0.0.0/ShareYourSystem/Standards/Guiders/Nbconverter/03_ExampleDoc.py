#ImportModules
import ShareYourSystem as SYS
from ShareYourSystem.Guiders import Nbconverter

#Definition a Nbconverter
MyNbconverter=Nbconverter.NbconverterClass().package(
		'ShareYourSystem.Standards.Objects.Concluder'
	).scriptbook(
		**{
			'GuidingBookStr':'Doc'
		}
	).notebook(
		'Presentation.ipynb'
	).nbconvert(
		'Readme.md',
		'Slide'
)
		
#Definition the AttestedStr
SYS._attest(
	[
		'MyNbconverter is '+SYS._str(
		MyNbconverter,
		**{
			'RepresentingBaseKeyStrsListBool':False,
			'RepresentingAlineaIsBool':False
			}
		)
	]
)  

#Print


