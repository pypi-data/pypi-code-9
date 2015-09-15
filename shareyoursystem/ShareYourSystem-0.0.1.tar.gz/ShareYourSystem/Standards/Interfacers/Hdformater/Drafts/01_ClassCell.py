
#FrozenIsBool False

#ImportModules
import ShareYourSystem as SYS
from ShareYourSystem.Standards.Objects.Hdformater import Drafts
		
#Definition the AttestedStr
SYS._attest(
	[
		'DefaultAttributeItemTuplesList is '+SYS._str(
			Drafts.DraftsClass.DefaultAttributeItemTuplesList,
			**{'RepresentingAlineaIsBool':False}
		)
	]
) 

#Print

