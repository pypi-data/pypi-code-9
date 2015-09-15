
#ImportModules
import ShareYourSystem as SYS
from ShareYourSystem.Standards.Modelers import Explorer
import tables

#Definition a structure with a db
ThingsExplorer=Explorer.ExplorerClass()

#Definition the AttestedStr
SYS._attest(
	[
		'ThingsExplorer is '+SYS._str(
		ThingsExplorer,
		**{
			'RepresentingBaseKeyStrsListBool':False,
			'RepresentingAlineaIsBool':False
		}
		),
		'hdf5 file is : '+ThingsExplorer.hdfview().hdfclose().HdformatedConsoleStr
	]
) 

#Print


