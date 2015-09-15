
#ImportModules
import ShareYourSystem as SYS

#Define a Sumer class
@SYS.ClasserClass()
class SumerClass(SYS.ControllerClass):
								
	def default_init(self,
						_SumingFirstInt=0,
						_SumingSecondInt=0,
						_SumedTotalInt=0,
						**_KwargVariablesDict
					):

		#Call the parent init method
		self.__class__.__bases__[0].__init__(self,**_KwargVariablesDict)
						
	def do_sum(self):
		
		#debug
		'''
		self.debug(('self.',self,['SumingFirstInt','SumingSecondInt']))
		'''

		#set the SumedTotalInt
		self.SumedTotalInt=self.SumingFirstInt+self.SumingSecondInt

#Definition of a Storer instance with a noded data
MySumer=SumerClass(
		**{
				'HdformatingFileKeyStr':'Sums_2.hdf5',
				'FolderingPathVariable':SYS.Joiner.LocalFolderPathStr
			}
	).collect(
		"Joiners",
		"Parameters",
		SYS.JoinerClass().update(
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
	).collect(
		"Joiners",
		"Results",
		SYS.JoinerClass().update(
			[
				(
					'Attr_ModelingDescriptionTuplesList',
					[
						('SumedTotalInt','SumedTotalInt',tables.Int64Col())
					]
				),
				('ConnectingGraspClueVariablesList',
					[
						'/NodePointDeriveNoder/<Joiners>ParametersJoiner'
					]
				),
				('TagStr','Networked')
			]
		)
	).network(
		**{
			'RecruitingConcludeConditionVariable':[
				(
					'MroClassesList',
					operator.contains,
					SYS.JoinerClass
				)
			]
		}
	)

#Update and store
MySumer.update(
		[
			('SumingFirstInt',1),
			('SumingSecondInt',3)
		]
	).sum(
	)['<Joiners>ParametersJoiner'].insert(
)

#Definition the AttestedStr
SYS._attest(
	[
		'MySumer is '+SYS._str(
		MySumer,
		**{
			'RepresentingBaseKeyStrsListBool':False,
			'RepresentingAlineaIsBool':False
		}
		),
		'hdf5 file is : '+MySumer.hdfview()
	]
) 

#close
MySumer.hdfclose()