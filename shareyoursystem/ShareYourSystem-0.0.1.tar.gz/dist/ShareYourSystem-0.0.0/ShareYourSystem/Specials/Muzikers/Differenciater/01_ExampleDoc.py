
#ImportModules
import ShareYourSystem as SYS
from ShareYourSystem.Muzikers import Differenciater

#Definition a Differenciater
MyDifferenciater=Differenciater.DifferenciaterClass().differenciate(
	**{
		'PermutingSubsetContentInt':3,
		'PermutingSetLengthInt':7
	})

#Definition the AttestedStr
SYS._attest(
	[
		'MyDifferenciater is '+SYS._str(
		MyDifferenciater,
		**{
			'RepresentingBaseKeyStrsListBool':False,
			'RepresentingAlineaIsBool':False
		}
		),
		'MyDifferenciater.hdfview().HdformatedConsoleStr is '+MyDifferenciater.hdfview().HdformatedConsoleStr
	]
) 

#Print

