
#ImportModules
import ShareYourSystem as SYS
from ShareYourSystem.Tutorials import Modulizer

#Definition a Modulizer
MyModulizer=Modulizer.ModulizerClass().update([

										(
											'<Output>RealMultiplier/update',
											{
												'LiargVariablesList':[
													[
														('MultiplyingFirstInt',2),
														('MultiplyingSecondInt',1),
													]
												]	
											}
										),
										(
											'<Output>ImageMultiplier/update',
											{
												'LiargVariablesList':[
													[
														('MultiplyingFirstInt',1),
														('MultiplyingSecondInt',1),
													]
												]
											}
										)
									]).modulize()

#Definition the AttestedStr
SYS._attest(
	[
		'MyModulizer is '+SYS._str(
		MyModulizer,
		**{
			'RepresentingBaseKeyStrsListBool':False,
			'RepresentingAlineaIsBool':False
		}
		)
	]
) 

#Print

