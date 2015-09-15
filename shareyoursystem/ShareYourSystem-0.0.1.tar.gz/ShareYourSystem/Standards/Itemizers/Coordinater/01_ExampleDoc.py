#ImportModules
import ShareYourSystem as SYS
import scipy.stats

#Define
@SYS.ClasserClass(**{
	'ClassingStructureVariable':[
		('Point','Points')
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

	def makeDownToUpPoint(self):
		
		#debug
		self.debug(
			[
				"We then makeDownToUpPoint first"
			]
		)

		#abs
		self.MadeDistanceFloat = abs(self.MakingCoordinateFloat)


EuclidianMaker = SYS.MakerClass(
	).mapSet(
		{
			"MakingCoordinateFloat":3.,
			"/-Points/|X/MakingCoordinateFloat":1.,
			"/-Points/|Y/MakingCoordinateFloat":-2.
		}
	).coordinate(
		"make"
	)

#print
print('EuclidianMaker is ')
SYS._print(EuclidianMaker)