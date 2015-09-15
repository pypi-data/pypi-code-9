#ImportModules
import ShareYourSystem as SYS
import numpy as np
import operator

#Define a Sumer class
@SYS.ClasserClass()
class SumerClass(SYS.OrganizerClass):

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
					):

		#Call the parent init method
		SYS.OrganizerClass.__init__(self)
		
	def do_sum(self):
		
		#debug
		'''
		self.debug(('self.',self,['SumingFirstInt','SumingSecondInt']))
		'''

		#set the SumedTotalInt
		self.SumedTotalInt=self.SumingFirstInt+self.SumingSecondInt

#Define a Factorizer class
@SYS.ClasserClass()
class FactorizerClass(SYS.OrganizerClass):

	#Definition
	RepresentingKeyStrsList=[
								'FactorizingPowerFloat',
								'FactorizedFloatsArray',
								'FactorizedTotalFloat',
								'FactorizedTotalStr'
							]
								
	def default_init(self,
						_FactorizingPowerFloat=1.,
						_FactorizedFloatsArray=None,
						_FactorizedTotalFloat=0.,
						_FactorizedTotalStr="",
					):

		#Call the parent init method
		SYS.OrganizerClass.__init__(self)

		#Build the output hierarchy
		self.produce(
				self.OrganizingComponentsCollectionStr,
				['X','Y'],
				SumerClass
			)

	def do_factorize(self):

		#debug
		'''
		self.debug('We factorize here')
		'''

		#Pick
		self.FactorizedFloatsArray=np.array(
			map(
					lambda __DeriveSumer:
					__DeriveSumer.SumedTotalInt,
					self['<Components>']
				)
		)

		#set the FactorizedTotalFloat
		self.FactorizedTotalFloat=np.power(
			sum(
				self.FactorizedFloatsArray
			),
			self.FactorizingPowerFloat
		)

		#set
		self.FactorizedTotalStr=str(self.FactorizedTotalFloat)

#Definition of a Factorizer instance, organize structure and network
MyFactorizer=FactorizerClass(
		**{
			'FolderingPathVariable':SYS.Organizer.LocalFolderPathStr
		}
	).walk(
		{
			'AfterUpdateList':[
				(
					'organize',
					SYS.ApplyDictClass()
				)
			],
			'GatherVariablesList':['<Components>']
		}
	).structure(
		['Components']
	).network(
		**{
			'VisitingCollectionStrsList':[
				'Models','Components'
			],
			'RecruitingConcludeConditionVariable':[
				(
					'MroClassesList',
					operator.contains,
					SYS.HierarchizerClass
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
			('callDo',SYS.ApplyDictClass({'LiargVariablesList':[]}))
		],
		'GatherVariablesList':['<Components>']
	}
)['<Models>ResultsHierarchizer'].insert()

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
)['<Models>ResultsHierarchizer'].insert()

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

