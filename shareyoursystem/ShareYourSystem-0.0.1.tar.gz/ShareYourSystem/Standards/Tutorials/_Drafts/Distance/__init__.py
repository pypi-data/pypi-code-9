#<ImportSpecificModules>
import ShareYourSystem as SYS
import numpy as np
import scipy.stats
from tables import *
import time
import operator
import os
#</ImportSpecificModules>

#<DefineLocals>
#</DefineLocals>

#<DefineClass>
class DistanceClass(SYS.ObjectsClass):

	#<DefineHookMethods>
	def initAfter(self):

		#<DefineSpecificDo>
		self.IntsList=[1,4,3]
		self.PowerFloat=0.5
		self.SquaredIntsList=[1,16,3]
		self.UnitsInt=3
		self.DistanceFloat=np.sqrt(sum(self.SquaredIntsList))
		#</DefineSpecificDo>

		#Definition the features
		self['App_Model_ParameterizingDict']={
										'ColumningTuplesList':
										[
											#ColumnStr 	#Col 	
											('PowerFloat',	Float64Col()),
											('IntsList',	(Int64Col,'UnitsInt'))
										],
										'IsFeaturingBool':True,
										'ScanningTuplesList':
										[
											('IntsList',[[1,2,3],[4,5]])
										]
									}

		#Definition the outputs
		self['App_Model_ResultingDict']={
										'ColumningTuplesList':
										[
											#ColumnStr 			#Col 
											('SquaredIntsList', 	(Int64Col,'UnitsInt')),
											('DistanceFloat',		Float64Col()),
											('IntsList',			(Int64Col,'UnitsInt'))
										],
										'JoiningTuple':("","Parameter")
									}
						
	def outputAfter(self,**_LocalOutputingVariablesDict):
		
		#set the SquaredIntsList
		self.SquaredIntsList=map(lambda __Int:__Int**2,self.IntsList)

		#set the DistanceFloat
		self.DistanceFloat=np.power(sum(self.SquaredIntsList),self.PowerFloat)

	#</DefineHookMethods>
	
	#</DefineTriggeringHookMethods>
	def bindIntsListAfter(self):

		#Bind with UnitsInt setting
		self.UnitsInt=len(self.IntsList)

	#</DefineTriggeringHookMethods>

#</DefineClass>

#<DefineAttestingFunctions>
def attest_insert():

	#Insert the default output
	Distance=SYS.DistanceClass(
		).update(
					[
						('IntsList',[4,5]),
						('PowerFloat',0.5)
					]
		).insert('Result'
		).update(
					[
						('IntsList',[4,5]),
						('PowerFloat',1.)
					]
		).insert(
		).update(
					[
						('IntsList',[4,5]),
						('PowerFloat',2.)
					]
		).insert(
		).update(
					[
						('IntsList',[1,2,3]),
						('PowerFloat',0.5)
					]
		).insert(
		).update(
					[
						('IntsList',[4,6]),
						('PowerFloat',1.)
					]
		).insert(
		).update(
					[
						('IntsList',[1,2,3]),
						('PowerFloat',1.)
					]
		).insert( 
		).update(
					[
						('IntsList',[0,1]),
						('PowerFloat',0.5)
					]
		).insert( 
		).hdfclose()

	#Return the object and the h5py
	return "\n\n\n\n"+SYS.represent(
			Distance
		)+'\n\n\n'+SYS.represent(
				os.popen('/usr/local/bin/h5ls -dlr '+Distance.HdformatingPathStr).read()
			)

def attest_retrieve():
	Distance=SYS.DistanceClass(
		).__setitem__('/App_Model_ResultingDict/RetrievingIndexesList',(0,2)
		).retrieve('Result'
		).hdfclose()

	#Return the object and the h5py
	return "\n\n\n\n"+SYS.represent(
			Distance
		)

def attest_find():
	Distance=SYS.DistanceClass(
		).update(
					[
						('/App_Model_ParameterizingDict/FindingTuplesList',[
													('IntsList',(SYS.getIsEqualBool,[4,5])),
											]),
						('/App_Model_ResultingDict/update',
							[
								('MergingTuplesList',
												[
													('UnitsInt',(operator.eq,2))
												]
											),
								('FindingTuplesList',[
													('DistanceFloat',(operator.gt,30.)),
													#('__IntsList',(SYS.getIsEqualBool,[4,5])),
											])
							]
						)
					]
		).find('Result'
		).hdfclose()

	#Return the object and the h5py
	return "\n\n\n\n"+SYS.represent(
			Distance
		)

def attest_recover():

	Distance=SYS.DistanceClass(
		).update(
					[
						('/App_Model_ParameterizingDict/FindingTuplesList',[
													('IntsList',(SYS.getIsEqualBool,[4,5])),
													('PowerFloat',(SYS.getIsEqualBool,1.))
											]),
						('/App_Model_ResultingDict/update',
							[
								('MergingTuplesList',
												[
													('UnitsInt',(operator.eq,2))
												]
											),
								('FindingTuplesList',[
													('DistanceFloat',(operator.gt,30.)),
													#('__IntsList',(SYS.getIsEqualBool,[4,5])),
											])
							]
						)
					]
		).recover('Result'
		).hdfclose()

	#Return the object and the h5py
	return "\n\n\n\n"+SYS.represent(
			Distance
		)

def attest_scan():

	#Scan
	Distance=SYS.DistanceClass(
		).scan('Result'
		).hdfclose()

	#Return the object and the h5py
	return "\n\n\n\n"+SYS.represent(
			Distance
		)+'\n\n\n'+SYS.represent(
				os.popen('/usr/local/bin/h5ls -dlr '+Distance.HdformatingPathStr).read()
			)
#</DefineAttestingFunctions>
