#ImportModules
import ShareYourSystem as SYS
import numpy as np

#Define a Sumer class
@SYS.ClasserClass()
class SumerClass(SYS.StorerClass):

	#Definition
	RepresentingKeyStrsList=[
								'SumingFirstInt',
								'SumingSecondInt',
								'SumedTotalInt'
							]
								
	def default_init(self,
						_SumingFirstInt=0,
						_SumingSecondInt=0,
						_SumedTotalInt=0
					):

		#Call the parent init method
		self.__class__.__bases__[0].__init__(self)
		
	def do_sum(self):
		
		#set the SumedTotalInt
		self.SumedTotalInt=self.SumingFirstInt+self.SumingSecondInt

#Define a Factorizer class
@SYS.ClasserClass()
class FactorizerClass(SYS.StorerClass):

	#Definition
	RepresentingKeyStrsList=[
								'FactorizingPowerFloat',
								'FactorizedTotalFloat'
							]
								
	def default_init(self,
						_FactorizingPowerFloat=1.,
						_FactorizedTotalFloat=0.
					):

		#Call the parent init method
		SYS.StorerClass.__init__(self)

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

		#set the FactorizedTotalFloat
		self.FactorizedTotalFloat=np.power(
			sum(
				map(
					lambda __DeriveSumer:
					__DeriveSumer.SumedTotalInt,
					self[self.OrganizedComponentsGetStr]
				)
			),
			self.FactorizingPowerFloat
		)

#Definition of a Factorizer 
MyFactorizer=FactorizerClass(
		**{
			#'HdformatingFileKeyStr':"Datome.hdf5",
			'FolderingPathVariable':SYS.Storer.LocalFolderPathStr
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
).store()

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
).store()

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

