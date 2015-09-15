#ImportSpecificModules
import ShareYourSystem as SYS
import ShareYourSystem as SYS
from ShareYourSystem.Standards.Objects import Celler

#Definition a Celler instance
MyCeller=Celler.CellerClass(
	**{
		#'FolderingPathVariable':SYS.__file__.split('__init__.py')[0]+'/Objects/Celler'
	}
).cell()

#Definition the AttestedStr
SYS._attest(
	[
		'MyCeller is '+SYS._str(
		MyCeller,
		**{
			'RepresentingBaseKeyStrsListBool':False
		}
		)
	]
)  

#Print


