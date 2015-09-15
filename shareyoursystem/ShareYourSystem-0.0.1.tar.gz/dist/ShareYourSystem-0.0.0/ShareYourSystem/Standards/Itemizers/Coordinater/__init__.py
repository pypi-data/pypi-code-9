# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>



"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Structurer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo('Coordinater','Coordinate','Coordinating','Coordinated')
#</DefineAugmentation>

#<ImportSpecificModules>
#</ImportSpecificModules>

#<DefineLocals>
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class CoordinaterClass(BaseClass):
	
	def default_init(
					self,	
					_CoordinatingMethodVariable = None,	
					_CoordinatingStructureBool = False,
					_CoordinatedMethodStrsList = None,	
					_CoordinatedParentSingularStr = "",	
					_CoordinatedTeamStrsList = None,
					_CoordinatedTopVariable	= None,
					_CoordinatedParentVariable = None,	
					_CoordinatedUpToDownBool = True,	
					_CoordinatedTopBool = False,	
					_CoordinatedTagStr = "",			
					**_KwargVariablesDict
				):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_coordinate(self):
		""" """

		#debug
		'''
		self.debug(
			[
				('self.',self,['CoordinatingMethodVariable'])
			]
		)
		'''

		#Check
		if type(self.CoordinatingMethodVariable)==str:
			self.CoordinatedMethodStrsList = [self.CoordinatingMethodVariable]
		else:
			self.CoordinatedMethodStrsList = self.CoordinatingMethodVariable

		#DefaultDoFunction
		map(
			lambda __CoordinatingMethodStr:
			setattr(
				self.__class__,
				__CoordinatingMethodStr,
				self.__class__.doCoordinateMethod
			) if getattr(
				self,
				"do_"+__CoordinatingMethodStr
			).__name__=="DefaultDoFunction"
			else None,
			self.CoordinatedMethodStrsList
		)
			
		#/###############/#
		# Parent Top case
		#

		#Check
		if self.ParentDeriveTeamerVariable == None:
			self.CoordinatedTagStr = "Top"
		else:
			self.CoordinatedTagStr = SYS.getSingularStrWithPluralStr(
				self.ParentDeriveTeamerVariable.TeamTagStr
			) 
			
		#debug
		'''
		self.debug(
			[
				"self.TeamingClassesDict is "+str(
					self.TeamingClassesDict
				)
			]
		)
		'''
		
		#DefaultDoFunction
		map(
			lambda __CoordinatingTopMethodStr:
			getattr(self,__CoordinatingTopMethodStr)()
			if hasattr(self,__CoordinatingTopMethodStr)
			else None,
			map(
				lambda __CoordinatingMethodStr:
				__CoordinatingMethodStr+"UpToDown"+self.CoordinatedTagStr,
				self.CoordinatedMethodStrsList
			)
		)

		#/###############/#
		# structure
		#

		#set
		self.CoordinatedTopBool = True

		#structure
		self.CoordinatingStructureBool = True
		self.structure()
		self.CoordinatingStructureBool = False

		#DefaultDoFunction
		map(
			lambda __CoordinatingTopMethodStr:
			getattr(self,__CoordinatingTopMethodStr)()
			if hasattr(self,__CoordinatingTopMethodStr)
			else None,
			map(
				lambda __CoordinatingMethodStr:
				__CoordinatingMethodStr+"DownToUp"+self.CoordinatedTagStr,
				self.CoordinatedMethodStrsList
			)
		)

	def doCoordinateMethod(self):

		#debug
		'''
		self.debug(
			[
				"We do the doCoordinateMethod"
			]
		)
		'''

		#Check
		if self.ParentDeriveTeamerVariable != None:

			#/##############/#
			# UpToDown call
			# 

			#Check
			if self.CoordinatedUpToDownBool:

				#set
				self.CoordinatedParentVariable = self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

				#/###############/#
				# UpToDown Component Case
				#

				#Check
				if self.ParentedTotalSingularListDict!=None and len(
					self.ParentedTotalSingularListDict
				)>0:

					#get
					self.CoordinatedParentSingularStr = self.ParentedTotalSingularListDict.keys()[0]
					if self.StructureTopDeriveStructurerRigidVariable!=None:
						self.CoordinatedTopVariable = self.StructureTopDeriveStructurerRigidVariable

					#set
					CoordinatedUpToDownMethodStrsList = map(
							lambda __hookStr:
							__hookStr+"UpToDown"+self.CoordinatedParentSingularStr,
							self.CoordinatedTopVariable.StructuringManagerCommandSetList
						)

					#debug
					'''
					self.debug(
						[
							('self.',self,[
									'CoordinatedParentSingularStr',
									#'StructureTopDeriveStructurerRigidVariable',
									'StructuringManagerCommandSetList'
								]
							),
							"CoordinatedUpToDownMethodStrsList is "+str(
								CoordinatedUpToDownMethodStrsList)
						]
					)
					'''

					#map
					map(
						lambda __methodStr:
						getattr(self,__methodStr)() 
						if hasattr(self,__methodStr) else None,
						CoordinatedUpToDownMethodStrsList	
					)

				#/###############/#
				# UpToDown Component Case
				#

				#Check
				if self.CoordinatedUpToDownBool==False or self.ManagementIndexInt==(
					len(self.ParentDeriveTeamerVariable.ManagementDict)-1
				) and all(
					map(
						lambda __TeamStr:
						__TeamStr not in self.CoordinatedTopVariable.CoordinatedTeamStrsList,
						self.TeamDict.keys()
					)
				):

					#set
					CoordinatedDownToUpMethodStrsList = map(
							lambda __hookStr:
							__hookStr+"DownToUp"+self.CoordinatedParentVariable.CoordinatedParentSingularStr,
							self.CoordinatedTopVariable.StructuringManagerCommandSetList
						)

					#debug
					'''
					self.debug(
						[
							"This is a last leaf in the coordinate or a DownToUp call",
							('self.',self,[
									#'CoordinatedParentVariable',
									'CoordinatedUpToDownBool'
								]),
							"CoordinatedDownToUpMethodStrsList is "+str(
								CoordinatedDownToUpMethodStrsList
							)
						]
					)
					'''

					#set
					self.CoordinatedParentVariable.CoordinatedUpToDownBool = False

					#map
					map(
						lambda __methodStr:
						getattr(
							self.CoordinatedParentVariable,
							__methodStr
						)() 
						if hasattr(self.CoordinatedParentVariable,__methodStr) else None,
						CoordinatedDownToUpMethodStrsList
					)

					#call
					self.CoordinatedParentVariable.doCoordinateMethod()

					#set
					self.CoordinatedUpToDownBool = True

	def mimic_structure(self):

		#Check
		if self.CoordinatingStructureBool and self.ParentDeriveTeamerVariable == None:

			#Check
			if self.CoordinatedTopBool:

				#/###############/#
				# Parent Top case
				#

				#debug
				'''
				self.debug(
					[
						"We structure coordinate the top here",
						('self.',self,[
							'CoordinatedMethodStrsList',
							'CoordinatedTeamStrsList'
						]),
						str(self.StructuresOrderedDict)
					]
				)
				'''

				#Check
				if self.CoordinatedMethodStrsList==None:
					self.CoordinatedMethodStrsList=self.StructuringManagerCommandSetList

				#debug
				self.CoordinatedTeamStrsList=list(
					set(
						SYS.sum(
							map(
								lambda __CoordinatedMethodStr:
								self.StructuresOrderedDict[
									__CoordinatedMethodStr
								].keys() if __CoordinatedMethodStr in self.StructuresOrderedDict
								else [],
								self.CoordinatedMethodStrsList
							)
						)
					)
				)

				#debug
				'''
				self.debug(
					[
						('self.',self,[
								'CoordinatedTeamStrsList'
							])
					]
				)
				'''

				#Check
				if len(self.CoordinatedTeamStrsList)>0: 

					#call
					BaseClass.structure(
						self,
						self.CoordinatedTeamStrsList,
						"#all",
						_ManagerCommandSetList=self.CoordinatedMethodStrsList
					)

		else:

			#normal
			BaseClass.structure(self)

			
#</DefineClass>

#<DefineLocals>
#<DefineLocals>

#</DefinePrint>
CoordinaterClass.PrintingClassSkipKeyStrsList.extend(
	[
		"CoordinatingMethodVariable",	
		"CoordinatingStructureBool",
		"CoordinatedMethodStrsList",
		"CoordinatedParentSingularStr",
		"CoordinatedTeamStrsList",
		"CoordinatedTopVariable",
		"CoordinatedTopBool",
		"CoordinatedTagStr"
	]
)
#<DefinePrint>
