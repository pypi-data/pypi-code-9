
#ImportModules
import ShareYourSystem as SYS

#Definition a "graph" structure
MyStructurer=SYS.StructurerClass().update(
	[
		(
			'<Graph>ChildStructurer1',
			Structurer.StructurerClass().update(
			[
				('<Graph>GrandChildStructurer1',
				Structurer.StructurerClass())
			])
		),
		(
			'<Graph>ChildStructurer2',
			Structurer.StructurerClass()
		)
	]	
).structure(**{
					'HdformatingFileKeyStr':'MyStructurer.hdf5',
					'ParentingNodeStr':'Graph'
			}).hdfclose()
		
#Definition the AttestedStr
SYS._attest(
	[
		'MyStructurer is '+SYS._str(
		MyStructurer,
		**{
			'RepresentingBaseKeyStrsListBool':False,
			'RepresentingAlineaIsBool':False
		}
		),
		'MyStructurer.hdfview().HdformatedConsoleStr is '+MyStructurer.hdfview().HdformatedConsoleStr
	]
) 

#Print

