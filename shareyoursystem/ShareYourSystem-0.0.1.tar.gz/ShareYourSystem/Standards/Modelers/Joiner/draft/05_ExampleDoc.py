#ImportModules
import ShareYourSystem as SYS
import operator
import tables
import numpy as np

#Define a Multiplier class
@SYS.ClasserClass()
class MultiplierClass(SYS.ControllerClass):

	#Definition
	RepresentingKeyStrsList=[
								'MultiplyingFirstInt',
								'MultiplyingSecondInt'
							]
								
	def default_init(self,
						_MultiplyingFirstInt=0,
						_MultiplyingSecondInt=0,
						**_KwargVariablesDict
					):

		#Call the parent init method
		SYS.ControllerClass.__init__(self,**_KwargVariablesDict)

		#Set a parameters database
		self.collect(
						"Joiners",
						"Parameters",
						SYS.JoinerClass().update(
							[
								(
									'Attr_ModelingDescriptionTuplesList',
									[
										('MultiplyingFirstInt','MultiplyingFirstInt',tables.Int64Col()),
										('MultiplyingSecondInt','MultiplyingSecondInt',tables.Int64Col())
									]
								),
								('Attr_RowingKeyStrsList',['MultiplyingFirstInt','MultiplyingSecondInt'])
							]
						)
				)
		
#Define a Modulizer class
@SYS.ClasserClass()
class ModulizerClass(SYS.ControllerClass):

	#Definition
	RepresentingKeyStrsList=[
									'ModulizingPowerFloat',
									'ModulizedTotalFloat'
								]
								
	def default_init(self,
						_ModulizingPowerFloat=1.,
						_ModulizedTotalFloat=0.,
						**_KwargVariablesDict
					):

		#Call the parent init method
		SYS.ControllerClass.__init__(self,**_KwargVariablesDict)

		#Build the output hierarchy
		self.update(
						[
							('<Components>RealMultiplier',MultiplierClass()),
							('<Components>ImageMultiplier',MultiplierClass())
						]
					)

		#Set a parameters database
		self.collect(
					"Joiners",
					"Parameters",
					SYS.JoinerClass().update(
						[
							(
								'Attr_ModelingDescriptionTuplesList',
								[
									('ModulizingPowerFloat','ModulizingPowerFloat',tables.Float64Col())
								]
							),
							('Attr_RowingKeyStrsList',['ModulizingPowerFloat']),
							('ConnectingGraspClueVariablesList',
								[
									'/NodePointDeriveNoder/<Components>RealMultiplier/<Joiners>ParametersJoiner',
									'/NodePointDeriveNoder/<Components>ImageMultiplier/<Joiners>ParametersJoiner'
								]
							)
						]
					)
				)


#Definition of a Modulizer instance, structure and network
MyModulizer=ModulizerClass(
		**{
			'FolderingPathVariable':SYS.Joiner.LocalFolderPathStr
		}
	).hdformat(
		'Modulizers.hdf5'
	).structure(
		['Components'],
		[
			('group',SYS.ApplyDictClass())
		],
		['HdformatedFileVariable']
	).network(
		**{
			'VisitingCollectionStrsList':['Joiners','Components'],
			'RecruitingConcludeConditionVariable':[
				(
					'MroClassesList',
					operator.contains,SYS.JoinerClass
				)
			]
		}
	)

#Update and insert in the results
MyModulizer.__setitem__(
	"Dis_<Components>",
	[
		[
			('MultiplyingFirstInt',1),
			('MultiplyingSecondInt',2)
		],
		[
			('MultiplyingFirstInt',1),
			('MultiplyingSecondInt',3)
		]
	]
)['<Joiners>ParametersJoiner'].insert()

#Update and insert in the results
MyModulizer.__setitem__(
	"Dis_<Components>",
	[
		[
			('MultiplyingFirstInt',2)
		],
		[
			('MultiplyingSecondInt',4)
		]
	]
)['<Joiners>ParametersJoiner'].insert()


#Definition the AttestedStr
SYS._attest(
	[
		'MyModulizer is '+SYS._str(
		MyModulizer,
		**{
			'RepresentingBaseKeyStrsListBool':False,
			'RepresentingAlineaIsBool':False
		}
		),
		'hdf5 file is : '+MyModulizer.hdfview()
	]
) 

#Close
MyModulizer.close()

