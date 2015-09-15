#ImportModules
import ShareYourSystem as SYS
import operator
import tables
import numpy as np

#Define a Sumer class
@SYS.ClasserClass()
class SumerClass(SYS.ControllerClass):

	#Definition
	RepresentingKeyStrsList=[
									'SumingFirstInt',
									'SumingSecondInt',
									'SumedTotalInt'
								]
								
	def default_init(self,
						_SumingFirstInt=0,
						_SumingSecondInt=0,
						_SumedTotalInt=0,
						**_KwargVariablesDict
					):

		#Call the parent init method
		SYS.ControllerClass.__init__(self,**_KwargVariablesDict)

		#Set a parameters database
		self.collect(
				"Hierarchizers",
				"Parameters",
				SYS.HierarchizerClass().update(
					[
						(
							'Attr_ModelingDescriptionTuplesList',
							[
								('SumingFirstInt','SumingFirstInt',tables.Int64Col()),
								('SumingSecondInt','SumingSecondInt',tables.Int64Col())
							]
						),
						('Attr_RowingKeyStrsList',['SumingFirstInt','SumingSecondInt'])
					]
				)
			)

		#Set a results database
		self.collect(
			"Hierarchizers",
			"Results",
			SYS.HierarchizerClass().update(
				[
					(
						'Attr_ModelingDescriptionTuplesList',
						[
							('SumedTotalInt','SumedTotalInt',tables.Int64Col())
						]
					),
					('ConnectingGraspClueVariablesList',
						[
							'/NodePointDeriveNoder/<Hierarchizers>ParametersHierarchizer'
						]
					),
					('TagStr','Networked')
				]
			)
		)
		
	def do_sum(self):
		
		#debug
		'''
		self.debug(('self.',self,['SumingFirstInt','SumingSecondInt']))
		'''

		#set the SumedTotalInt
		self.SumedTotalInt=self.SumingFirstInt+self.SumingSecondInt

#Define a Factorizer class
@SYS.ClasserClass()
class FactorizerClass(SYS.ControllerClass):

	#Definition
	RepresentingKeyStrsList=[
								'FactorizingPowerFloat',
								'FactorizedTotalFloat'
							]
								
	def default_init(self,
						_FactorizingPowerFloat=1.,
						_FactorizedTotalFloat=0.,
						**_KwargVariablesDict
					):

		#Call the parent init method
		SYS.ControllerClass.__init__(self,**_KwargVariablesDict)

		#Build the output hierarchy
		self.update(
						[
							('<Components>XSumer',SumerClass()),
							('<Components>YSumer',SumerClass())
						]
					)

		#Set a parameters database
		self.collect(
					"Hierarchizers",
					"Parameters",
					SYS.HierarchizerClass().update(
						[
							(
								'Attr_ModelingDescriptionTuplesList',
								[
									('FactorizingPowerFloat','FactorizingPowerFloat',tables.Float64Col())
								]
							),
							('Attr_RowingKeyStrsList',['FactorizingPowerFloat']),
							('ConnectingGraspClueVariablesList',
								[
									'/NodePointDeriveNoder/<Components>XSumer/<Hierarchizers>ParametersHierarchizer',
									'/NodePointDeriveNoder/<Components>YSumer/<Hierarchizers>ParametersHierarchizer'
								]
							)
						]
					)
				)

		#Set a results database
		self.collect(
			"Hierarchizers",
			"Results",
			SYS.HierarchizerClass().update(
				[
					(
						'Attr_ModelingDescriptionTuplesList',
						[
							('FactorizedTotalFloat','FactorizedTotalFloat',tables.Float64Col())
						]
					),
					('ConnectingGraspClueVariablesList',
						[
							'/NodePointDeriveNoder/<Hierarchizers>ParametersHierarchizer'
						]
					),
					('TagStr','Networked')
				]
			)
		)

	def do_factorize(self):

		#debug
		self.debug('We factorize here')

		#set the FactorizedTotalFloat
		self.FactorizedTotalFloat=np.power(
			sum(
				map(
					lambda __DeriveSumer:
					__DeriveSumer.SumedTotalInt,
					self['<Components>']
				)
			),
			self.FactorizingPowerFloat
		)

#Definition of a Factorizer instance, structure and network
MyFactorizer=FactorizerClass(
		**{
			'FolderingPathVariable':SYS.Hierarchizer.LocalFolderPathStr
		}
	).structure(
		['Components']
	).network(
		**{
			'VisitingCollectionStrsList':['Hierarchizers','Components'],
			'RecruitingConcludeConditionVariable':[
				(
					'MroClassesList',
					operator.contains,SYS.HierarchizerClass
				)
			]
		}
	)

#Update transmit the do method and insert in the results
MyFactorizer.__setitem__(
	"Dis_<Components>",
	[
		[
			('SumingFirstInt',1),
			('SumingSecondInt',2)
		],
		[
			('SumingFirstInt',1),
			('SumingSecondInt',3)
		]
	]
).walk(
	{
		'AfterUpdateList':[
			('callDo',{'LiargVariablesList':[]})
		],
		'GatherVariablesList':['<Components>']
	}
)['<Hierarchizers>ResultsHierarchizer'].insert()

#Update and insert in the results
MyFactorizer.__setitem__(
	"Dis_<Components>",
	[
		[
			('SumingFirstInt',2)
		],
		[
			('SumingSecondInt',4)
		]
	]
).walk(
	{
		'AfterUpdateList':[
			('callDo',{'LiargVariablesList':[]})
		],
		'GatherVariablesList':['<Components>']
	}
)['<Hierarchizers>ResultsHierarchizer'].insert()

#Definition the AttestedStr
SYS._attest(
	[
		'MyFactorizer is '+SYS._str(
		MyFactorizer,
		**{
			'RepresentingBaseKeyStrsListBool':False,
			'RepresentingAlineaIsBool':False
		}
		),
		'hdf5 file is : '+MyFactorizer.hdfview().hdfclose().HdformatedConsoleStr
	]
) 

#Print

