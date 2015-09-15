#ImportModules
import ShareYourSystem as SYS
import scipy.stats

#degine
@SYS.ClasserClass()
class MakerClass(SYS.ExplorerClass):

	def default_init(
					self,	
					_MakingXFloat = 0.,
					_MakingYFloat = 0.,
					_MadeDistanceFloat = 0., 													
					**_KwargVariablesDict
				):

		#Call the parent __init__ method
		SYS.ExplorerClass.__init__(self,**_KwargVariablesDict)

	def do_make(self):

		#compute
		self.MadeDistanceFloat = SYS.numpy.sqrt(self.MakingXFloat**2 + self.MakingYFloat**2)

		#debug
		'''
		self.debug(
			[
				('self.',self,['MadeDistanceFloat'])
			]
		)	
		'''


#Definition 
DiskMaker=SYS.MakerClass(
	).make(
		1.,2.
	).explore(
		_MethodStr = 'make',
		_SuccessesInt = 1000,
		_RangeVariable = {
			'MakingXFloat':lambda self:-1.+2.*scipy.stats.uniform.rvs(),
			'MakingYFloat':lambda self:-1.+2.*scipy.stats.uniform.rvs()
		},
		_ConditionVariable = {
			'checkDistanceFloat':lambda self:self.MadeDistanceFloat<1.
		}
	)

#print
print('DiskMaker is ')
SYS._print(DiskMaker)

#show
map(
	lambda __TuplesList:
	SYS.plot(*list(dict(__TuplesList).values()),marker='o'),
	DiskMaker.ExploredStoreTuplesListsList
)
SYS.show()