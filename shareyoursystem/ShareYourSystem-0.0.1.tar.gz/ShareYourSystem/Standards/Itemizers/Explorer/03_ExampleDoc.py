#ImportModules
import ShareYourSystem as SYS
import scipy.stats

#Define
@SYS.ClasserClass(**{
	'ClassingStructureVariable':[
		('Point','Points')
	]
})
class MakerClass(SYS.ExplorerClass):

	def default_init(
					self,
					_MakingCoordinateFloat = 0.,	
					_MadeDistanceFloat = 0., 													
					**_KwargVariablesDict
				):

		#Call the parent __init__ method
		SYS.ExplorerClass.__init__(self,**_KwargVariablesDict)

			
	def makeDownToUpTop(self):
		
		#/################/#
		# Way to compute things
		#

		#compute
		self.MadeDistanceFloat = sum(
				map(
					lambda __Variable:
					__Variable.MadeDistanceFloat,
					self.TeamDict['Points'].ManagementDict.values()
				)
			) - self.MakingCoordinateFloat**2

	def makeUpToDownPoint(self):
		
		#square
		self.MadeDistanceFloat = self.MakingCoordinateFloat**2

	def exploreTop(self):

		#set
		return self.MadeDistanceFloat < 0. 
		#return self.MadeDistanceFloat < 1.

	def explorePoint(self):

		#/################/#
		# Way to define the check
		#

		#set
		#return self.MadeDistanceFloat < self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable.MakingCoordinateFloat
		#return self.MadeDistanceFloat < 5.
		#return self.MakingCoordinateFloat > 0.
		return True

#Definition 
ConeMaker=SYS.MakerClass(
	).mapSet(
		{
			"ExploringRangeVariable":{
				"MakingCoordinateFloat":lambda self:4.*scipy.stats.uniform.rvs()
			},
			"-Points":{
				"ManagingAfterSetVariable":{
					"ExploringRangeVariable":{
						"MakingCoordinateFloat":lambda self:-2.+4.*scipy.stats.uniform.rvs()
					}
				},
				"|X":{
				},
				"|Y":{
				}
			}
		}
	).explore(
		_MethodStr = 'make',
		_SuccessesInt = 1000,
		_TrialsInt = 500
	)

#print
print('ConeMaker is ')
SYS._print(ConeMaker)

#show
map(
	lambda __ExploredTotalOrderedDict:
	SYS.scatter3D(
		__ExploredTotalOrderedDict['_Top_Points_X']['MakingCoordinateFloat'],
		__ExploredTotalOrderedDict['_Top_Points_Y']['MakingCoordinateFloat'],
		__ExploredTotalOrderedDict['MakingCoordinateFloat'],
		marker='o'
	).Axes.set_xlabel(
		"X"
	).set_ylabel(
		"Y"
	).set_zlabel(
		"Z"
	),
	ConeMaker.ExploredTotalOrderedDictsList
)
SYS.show()
