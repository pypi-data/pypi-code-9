# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>



"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Coordinater"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo('Explorer','Explore','Exploring','Explored')
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
#</ImportSpecificModules>

#<DefineLocals>
#</DefineLocals>

#<DefineClass>
@DecorationClass(**{})
class ExplorerClass(BaseClass):
	
	def default_init(
					self,	
					_ExploringMethodStr = "",
					_ExploringRangeVariable = None, 
					_ExploringConditionVariable = None,
					_ExploringTrialsInt = 1000, 
					_ExploringSuccessesInt = 1,
					_ExploredCheckBool = False,
					_ExploredParameterStrsList = None,
					_ExploredRangeTuplesList = None,
					_ExploredConditionTuplesList = None, 
					_ExploredKeepStrsList = None,	
					_ExploredStoreTuplesListsList = None,
					_ExploredTotalOrderedDictsList = None,
					_ExploredRigidTrialsInt = 0,
					_ExploredRigidSucessesInt = 0,
					_ExploredManagersVariable = None,
					_ExploredRigidMaxTrialBool = False,
					_ExploredRigidSuccessBool = False,
					_ExploredTeamStrsList = None, 
					_ExploredMethodStr="",											
					**_KwargVariablesDict
				):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_explore(self):
		""" """

		#debug
		'''
		self.debug(
			[
				"We explore here",
			]
		)
		'''

		#reinit
		self.ExploredRigidSucessesInt = 0
		self.ExploredRigidTrialsInt = 0
		self.ExploredRigidMaxTrialBool = False
		self.ExploredRigidSuccessBool = False

		#Check
		if self.ExploredRigidSucessesInt < self.ExploringSuccessesInt:

			#
			# Prepare
			#

			#Check
			if hasattr(self.ExploringRangeVariable,'items'):
				self.ExploredRangeTuplesList=self.ExploringRangeVariable.items()

			#Check
			if hasattr(self.ExploringConditionVariable,'items'):
				self.ExploredConditionTuplesList=self.ExploringConditionVariable.items()

			#Check
			if len(self.ExploredRangeTuplesList)!=len(self.ExploredParameterStrsList):
				self.ExploredParameterStrsList = map(
					lambda __TuplesList:__TuplesList[0],
					self.ExploredRangeTuplesList
				)


			#
			# Prepare Children
			#

			#Check
			if self.ExploredManagersVariable == None:

				#keys
				if self.DeriveClassor.ClassingStructureVariable!=None:
					if hasattr(self.DeriveClassor.ClassingStructureVariable,'items')==False:
						self.ExploredTeamStrsList = SYS.unzip(
							self.DeriveClassor.ClassingStructureVariable,[1]
						)
					else:
						self.ExploredTeamStrsList = self.DeriveClassor.ClassingStructureVariable.values()

				#debug
				'''
				self.debug(
					[
						('self.',self,[
								'TeamingClassesDict',
								'ExploredTeamStrsList'
							]),
						str(self.DeriveClassor.ClassingStructureVariable)
					]
				)
				'''
				
				#sum
				self.ExploredManagersVariable = SYS.sum(
					SYS.filterNone(
						map(
							lambda __TeamStr:
							self.TeamDict[__TeamStr].ManagementDict.values()
							if __TeamStr in self.TeamDict
							else None,
							self.ExploredTeamStrsList
						)
					)
				) if self.DeriveClassor.ClassingStructureVariable!=None else []

				#Check
				if self.ParentDeriveTeamerVariable == None:

					#debug
					'''
					self.debug(
						[
							"We coordinate one time"
						]
					)
					'''

					#coordinate one first time
					self.coordinate(self.ExploringMethodStr)

					#Check
					if hasattr(self,"exploreTop"):

						#append
						self.ExploredConditionTuplesList.append(
							('exploreTop',getattr(self.__class__,"exploreTop"))
						)

					#set
					ExploredTopMethodStr = self.ExploringMethodStr+"UpToDownTop"

					#Check
					if hasattr(self,ExploredTopMethodStr):

						#set
						self.ExploredMethodStr = ExploredTopMethodStr

			#Check
			if self.ExploredMethodStr=="":
				self.ExploredMethodStr = self.ExploringMethodStr

			#
			# Pick
			#

			#Check
			while self.ExploredRigidTrialsInt <= self.ExploringTrialsInt:

				#count
				self.ExploredRigidTrialsInt +=1

				#debug
				'''
				self.debug(
					[
						"We test with a new trial set",
						('self.',self,[
								'ExploredRigidTrialsInt',
								'ExploredRigidSucessesInt'
							])
					]
				)
				'''

				#
				# Init
				#

				#debug
				'''
				self.debug(
					[
						'First we range parameters',
						('self.',self,[
								'ExploredRangeTuplesList'
							])
					]
				)
				'''

				#init the ranges
				map(
					lambda __TuplesList:
					setattr(
						self,
						__TuplesList[0],
						__TuplesList[1](self)
					),
					self.ExploredRangeTuplesList
				)

				#
				# Test
				#

				#debug
				'''
				self.debug(
					[
						"Now we do the local test",
						('self.',self,[
								'ExploringMethodStr',
								'ExploredMethodStr'
							])
					]
				)
				'''
				
				#call
				if hasattr(self,self.ExploredMethodStr):
					getattr(self,self.ExploredMethodStr)()


				#
				# Check Children
				#

				#debug
				'''
				self.debug(
					[
						"We first check the children"
					]
				)
				'''

				#map
				ExploredBoolsList = map(
					lambda __Manager:
					__Manager.setAttr(
							"CoordinatingMethodStr",self.ExploringMethodStr
						).explore(
							_MethodStr = self.ExploringMethodStr.split(
								"UpToDown"+__Manager.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable.CoordinatedParentSingularStr
							)[0]+ "UpToDown" + __Manager.CoordinatedParentSingularStr if __Manager.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable.CoordinatedParentSingularStr!="" 
							else self.ExploringMethodStr + "UpToDown" + __Manager.CoordinatedParentSingularStr
							#_MethodStr="coordinate",
							,_ConditionVariable = SYS.update(
								self.ExploringConditionVariable,
								{
									"explore"+__Manager.CoordinatedParentSingularStr:getattr(
										self.__class__,
										"explore"+__Manager.CoordinatedParentSingularStr
									)
								}
							) 
							if hasattr(
								__Manager,
								"explore"+__Manager.CoordinatedParentSingularStr
							)
							else self.ExploringConditionVariable,
							_SuccessesInt=1
					).ExploredCheckBool
					#if __Manager.ExploredCheckBool==False
					#else None,
					,self.ExploredManagersVariable
				)

				#Check
				"""
				if all(ExploredBoolsList)==False:

					#debug
					'''
					self.debug(
						[
							"Children not correctly setted"
						]
					)
					'''
					pass
				"""

				
				#
				# Each Check
				#

				#init
				self.ExploredCheckBool = True

				#loop
				for __ConditionTuple in self.ExploredConditionTuplesList:

					#debug
					'''
					self.debug(
						[
							"__ConditionTuple is "+str(__ConditionTuple)
						]
					)
					'''

					#Check
					if __ConditionTuple[1](self) == False:

						#debug
						'''
						self.debug(
							"the check is not good"
						)
						'''

						#set
						self.ExploredCheckBool = False

						#break
						break


				#debug
				'''
				self.debug(
					[
						('self.',self,[
								'ExploredCheckBool'
							])
					]
				)
				'''

				#
				# Total Check
				#

				#Check
				if self.ExploredCheckBool:

					#
					# Say success
					#

					#count
					self.ExploredRigidSucessesInt += 1

					#
					# Append
					#

					#keep
					self.ExploredStoreTuplesListsList.append(
						map(
							lambda __KeyStr:
							(__KeyStr,getattr(self,__KeyStr)),
							self.ExploredKeepStrsList+self.ExploredParameterStrsList
						)
					)

					#debug
					'''
					self.debug(
						[
							"it is a sucess",
							#('self.',self,['ExploredStoreTuplesListsList'])
						]
					)
					'''

				else:

					#
					# Remove last store in children
					#

					#map
					map(
						lambda __ManagerVariable:
						__ManagerVariable.ExploredStoreTuplesListsList.pop(),
						self.ExploredManagersVariable
					)


				#
				# Reset children
				#

				#map
				map(
					lambda __ManagerVariable:
					setattr(
						__ManagerVariable,
						"ExploredCheckBool",
						False
					),
					self.ExploredManagersVariable
				)

				#break maybe
				if self.ExploredRigidSucessesInt >= self.ExploringSuccessesInt:
					
					#break
					break

			


			#Check
			if self.ExploredRigidTrialsInt > self.ExploringTrialsInt:
				
				#debug
				'''
				self.debug(
					[
						('We reached the max of Trials ot pick'),
						('self.',self,[
								'ExploringTrialsInt',
								'ExploredRigidTrialsInt',
								'ExploringSuccessesInt',
								'ExploredRigidSucessesInt'
							])
					]
				)
				'''
				
				#set
				self.ExploredRigidMaxTrialBool = True

		else:

			#debug
			'''
			self.debug(
				[
					('We reached the sufficient number of sucesses')
				]
			)
			'''

			#set
			self.ExploredRigidSuccessBool = True

		#
		# Build the total tree of explored parameters
		#

		#map
		self.ExploredTotalOrderedDictsList = map(
			lambda __IndexInt,__ExploredStoreTuplesList:
			collections.OrderedDict(
				map(
					lambda __ExploredManagerVariable:
					(
						__ExploredManagerVariable.ParentTagStr,
						collections.OrderedDict(
							__ExploredManagerVariable.ExploredStoreTuplesListsList[
								__IndexInt
							]
						)
					),
					self.ExploredManagersVariable
				),
				**collections.OrderedDict(__ExploredStoreTuplesList)
			),
			xrange(len(self.ExploredStoreTuplesListsList)),
			self.ExploredStoreTuplesListsList
		)


#</DefineClass>

#<DefineLocals>
#<DefineLocals>

#</DefinePrint>
ExplorerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'ExploringMethodStr',
		'ExploringTopMethodStr',
		'ExploringRangeVariable', 
		'ExploringConditionVariable', 
		'ExploringTrialsInt',
		'ExploringSuccessesInt',
		'ExploredRangeTuplesList',
		'ExploredConditionTuplesList',
		'ExploredParameterStrsList',
		'ExploredKeepStrsList',
		'ExploredCheckBool',
		'ExploredManagersVariable',
		'ExploredStoreTuplesListsList',
		'ExploredTotalOrderedDictsList',
		'ExploredRigidTrialsInt',
		'ExploredRigidSucessesInt',
		'ExploredRigidMaxTrialBool',
		'ExploredRigidSuccessBool',
		'ExploredTeamStrsList',
		'ExploredMethodStr'
	]
)
#<DefinePrint>
