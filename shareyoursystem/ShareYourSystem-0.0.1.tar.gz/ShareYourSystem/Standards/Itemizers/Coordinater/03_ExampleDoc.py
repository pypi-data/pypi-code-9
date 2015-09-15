#ImportModules
import ShareYourSystem as SYS
import scipy.stats

#Define
@SYS.ClasserClass(**{
	'ClassingStructureVariable':[
		('Point','Points'),
		('Color','Colors')
	]
})
class MakerClass(SYS.CoordinaterClass):

	def default_init(
					self,
					_MakingCoordinateFloat = 0.,	
					_MadeDistanceFloat = 0., 													
					**_KwargVariablesDict
				):

		#Call the parent __init__ method
		SYS.CoordinaterClass.__init__(self,**_KwargVariablesDict)
		
	def makeDownToUpTop(self):
		
		#debug
		self.debug(
			[
				"We makeDownToUpTop last"
			]
		)

		#compute
		self.MadeDistanceFloat = SYS.numpy.sqrt(
			sum(
				SYS.numpy.array(
					map(
						lambda __Variable:
						__Variable.MadeDistanceFloat,
						self.TeamDict['Points'].ManagementDict.values()
					)
				)**2
			)
		)

	def makeUpToDownPoint(self):
		
		#debug
		self.debug(
			[
				"We makeUpToDownPoint first"
			]
		)

		#abs
		self.MadeDistanceFloat = abs(self.MakingCoordinateFloat)

	def makeDownToUpPoint(self):
		
		#debug
		self.debug(
			[
				"We makeDownToUpPoint third"
			]
		)

	def makeUpToDownColor(self):

		#debug
		self.debug(
			[
				"We makeUpToDownColor second"
			]
		)

		#abs
		self.MadeDistanceFloat = abs(self.MakingCoordinateFloat)



EuclidianMaker = SYS.MakerClass(
	).mapSet(
		{
			"MakingCoordinateFloat":3.,
			"/-Points/|X":{
				"MakingCoordinateFloat":1.,
				"-Colors":{
					"/|Blue/MakingCoordinateFloat":15.,
					"/|Green/MakingCoordinateFloat":10.,
				}
			},
			"/-Points/|Y/MakingCoordinateFloat":-2.
		}
	)['/-Points/|X'].coordinate('make')

#print
print('EuclidianMaker is ')
SYS._print(EuclidianMaker)