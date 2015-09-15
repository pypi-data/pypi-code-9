# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Pointer 

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Parenter"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
from ShareYourSystem.Standards.Itemizers import Pather,Teamer,Manager,Parenter
#</ImportSpecificModules>

#<DefineLocals>
PointPrefixStr="*"
PointToStr="->"
PointBackStr="<->"
PointBackPrefixStr="Back"
PointInTeamStr="Inlets"
PointOutTeamStr="Outlets"
PointConnectKeyStr='?>'
def getLiargVariablesList(_ValueVariable):
	return _ValueVariable
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class PointerClass(BaseClass):

	def default_init(
					self,	
					_PointToVariable=None,
					_PointFromVariable=None,
					_PointingToGetVariable=None,
					_PointingToSetKeyVariable=None,
					_PointingBackSetKeyVariable=None,
					_PointingBackBool=False,
					_PointingManagementBool=True,
					_PointingEncapsulationBool=True,
					_PointedToVariable=None,
					**_KwargVariablesDict
				):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_point(self):

		#debug
		'''
		self.debug(
			[
				'we point here',
				('self.',self,[
								'PointingToGetVariable',
								'PointingToSetKeyVariable'
							])
			]
		)
		'''

		#Check
		if self.PointingToGetVariable!=None:

			#/###################/#
			# First point TO like a classic set
			#

			#debug
			self.debug(
				[
					'First we get the target',
					('self.',self,['PointingToGetVariable'])
				]
			)

			#get
			PointedToVariable=self[
				self.PointingToGetVariable
			]

			#debug
			'''
			self.debug(
				[
					'PointedToVariable is '+SYS._str(
						PointedToVariable
					),
					'If it is None, maybe we have to parent first'
				]
			)
			'''

			#Check
			"""
			if PointedToVariable==None:

				#parent
				self['?^']

				#debug
				self.debug(
						[
							'We have parented',
							('self.',self,['ParentedTotalPathStr']),
							'So we can get again'
						]
					)

				#get
				PointedToVariable=self[
					self.PointingToGetVariable
				]
			"""

			#debug
			'''
			self.debug(
				[
					'PointedToVariable is '+SYS._str(
						PointedToVariable
					),
					'Now we check the set key str'
				]
			)
			'''

			#/####################/#
			# Check for the SetKeyVariable
			#

			#Check
			if self.PointingToSetKeyVariable in [None,""]:

				#debug
				'''
				self.debug(
						[
							"self.PointingToSetKeyVariable in [None,""]...",
							"so we use the PointingGetVariable to name the pointer"
						]
					)
				'''

				#str
				PointedToSetKeyVariable=str(
						self.PointingToGetVariable
					).replace('/','_')

				#debug
				self.debug(
						[
							'PointedToSetKeyVariable is '+PointedToSetKeyVariable
						]
					)

				#Check
				if self.PointingManagementBool:

					#debug
					self.debug(
							[
								'We put that in the Management dict'
							]
						)

					#add
					PointedToSetKeyVariable=Manager.ManagementChildPrefixStr+PointedToSetKeyVariable

			else:

				#set direct
				PointedToSetKeyVariable=self.PointingToSetKeyVariable

			#debug
			'''
			self.debug(
					'PointedToSetKeyVariable is '+SYS._str(
						PointedToSetKeyVariable
					)
				)
			'''

			#Check
			if type(PointedToSetKeyVariable)==str and PointedToSetKeyVariable.endswith(
				Pather.PathPrefixStr)==False:

				#debug
				'''
				self.debug('It is a direct path')
				'''
				
				if self.PointingEncapsulationBool==False:

					#set
					self.set(
							PointedToSetKeyVariable,
							PointedToVariable
						)
				else:

					pass



			else:

				#debug
				'''
				self.debug(
					[
						'It is an encapsulate path',
						'PointedToSetKeyVariable is ',
						str(PointedToSetKeyVariable),
						'Check if it is with a str or a variable'
					]
				)
				'''

				#/###############/#
				# Case where it is just a default encapsulator
				#

				#Check
				if type(PointedToSetKeyVariable)==str:

					#previous
					PointedPreviousSetTagStr,PointedKeyStr=SYS.previous(
						PointedToSetKeyVariable
					)

					#debug
					self.debug(
						[
							'PointedPreviousSetTagStr is ',
							PointedPreviousSetTagStr,
							'PointedKeyStr is ',
							PointedKeyStr
						]
					)

					#Check
					if self.PointingManagementBool:

						#debug
						self.debug(
								[
									'We put that in the Management dict'
								]
							)

						#add
						PointedPreviousSetTagStr=Manager.ManagementChildPrefixStr+PointedPreviousSetTagStr

					#get
					PointedGettedValueVariable=self[
						PointedPreviousSetTagStr
					]

					#Check
					if PointedKeyStr!="":

						#debug
						self.debug(
								'We just set normally'
							)

						#point
						PointedGettedValueVariable.set(
								PointedKeyStr,
								PointedToVariable
							)

					else:

						#debug
						self.debug(
								'We set the PointToVariable and PointFromVariable'
							)

						#point
						PointedGettedValueVariable.set(
								'PointToVariable',
								PointedToVariable
							)

						#point
						PointedGettedValueVariable.set(
								'PointFromVariable',
								self
							)



			#debug
			'''
			self.debug(
						[
							'After getting',
							('locals()["',locals(),[
											'PointedToVariable',
											],']
										)
						]
					)
			'''

			#/###################/#
			# Maybe do a back point
			#

			#Check
			if self.PointingBackBool:

				#debug
				'''
				self.debug(
						[
							'We point back',
							('self.',self,['PointingBackSetKeyVariable'])
						]
					)
				'''

				#Check
				if self.PointingBackSetKeyVariable==None:
					
					#debug
					'''
					self.debug(
						'PointedToSetKeyVariable is '+str(PointedToSetKeyVariable)
					)
					'''

					#/###################/#
					# Case where the PointedToSetKeyVariable is derived from a pathsetstr
					#

					#split
					PointedKeyStrsList=PointedToSetKeyVariable.split('_')
					if len(PointedKeyStrsList)>1:

						#remove the last
						PointedKeyStrsList=PointedKeyStrsList[1:]

						#reverse
						PointedKeyStrsList.reverse()

						#join
						PointedBackSetKeyVariable='_'.join(PointedKeyStrsList)

					#/###################/#
					# else just take the id and put a prefix
					#

					else:

						#set default
						PointedBackSetKeyVariable=str(self.PrintIdInt)

					#add
					PointedBackSetKeyVariable=PointBackPrefixStr+PointedBackSetKeyVariable+self.NameStr

				else:

					#just alias
					PointedBackSetKeyVariable=self.PointingBackSetKeyVariable

				#debug
				self.debug(
						[
							'we set the back',
							'PointedBackSetKeyVariable is '+SYS._str(
								PointedBackSetKeyVariable
							),
							'PointedToVariable is '+SYS._str(
								PointedToVariable
							)
						]
					)

				#set
				PointedToVariable.point(
						self,
						PointedBackSetKeyVariable,
						_BackBool=False
					)

			#alias
			self.PointedToVariable=PointedToVariable

	def mimic_get(self):

		#debug
		'''
		self.debug(
				('self.',self,[
						'GettingKeyVariable',
					])
			)
		'''

		#Check
		if type(self.GettingKeyVariable)==str:

			#Check
			if self.GettingKeyVariable.startswith(
				PointToStr
			):

				#debug
				'''
				self.debug(
						'we point here'
					)
				'''

				#point
				self.point(
						SYS.deprefix(
							self.GettingKeyVariable,
							PointToStr
						)
					)

				#alias
				self.GettedValueVariable=self.PointedToVariable

				#return
				return {'HookingIsBool':False}

			elif self.GettingKeyVariable.startswith(
					PointBackStr
				):

				#debug
				'''
				self.debug(
						'we back point here'
					)
				'''

				#point
				self.point(
						SYS.deprefix(
							self.GettingKeyVariable,
							PointBackStr
						),
						_BackBool=True
					)

				#alias
				self.GettedValueVariable=self.PointedToVariable

				#return
				return {'HookingIsBool':False}

			elif self.GettingKeyVariable.startswith(
					PointPrefixStr
				):

				#debug
				'''
				self.debug(
						'we get the encapsulate variable'
					)
				'''

				#deprefix
				PointGetKeyStr=SYS.deprefix(
					self.GettingKeyVariable,
					PointPrefixStr
				)

				#get
				self.GettedValueVariable=self[PointGetKeyStr]['PointToVariable']

				#return
				return {'HookingIsBool':False}

		#call the base method
		return BaseClass.get(self)

	def mimic_set(self):

		#debug
		'''
		self.debug(
				('self.',self,[
						'SettingKeyVariable',
						'SettingValueVariable',
					])
			)
		'''

		#Check
		if type(self.SettingKeyVariable)==str:

			#Check
			if self.SettingKeyVariable.startswith(PointToStr):

				#debug
				'''
				self.debug(
						'we point just here'
					)
				'''

				#point
				self.point(
						SYS.deprefix(
							self.SettingKeyVariable,
							PointToStr
						),
						self.SettingValueVariable
					)

				#return
				return {'HookingIsBool':False}

			elif self.SettingKeyVariable.startswith(PointBackStr):

				#debug
				'''
				self.debug(
						'we point back here'
					)
				'''
				
				#point
				self.point(
						SYS.deprefix(
							self.SettingKeyVariable,
							PointBackStr
						),
						self.SettingValueVariable[0],
						_BackSetKeyVariable=self.SettingValueVariable[1],
						_BackBool=True
					)

				#return
				return {'HookingIsBool':False}

			'''
			elif self.SettingKeyVariable.startswith(PointPrefixStr):

				#debug
				self.debug(
						'we set in the encapsulate'
					)

				#set
				SettedValueVariable=self[
						self.SettingKeyVariable
					]

				#alias
				SettedValueVariable=self.SettingValueVariable
					

				#return
				return {'HookingIsBool':False}
			'''

		#debug
		'''
		self.debug(
				[
					'Call the base set method',
					'BaseClass is '+str(BaseClass),
					('self.',self,['SettingKeyVariable'])
				]
			)
		'''

		#call the base method
		return BaseClass.set(self)

	def mapPoint(self):

		#debug
		self.debug(
				[
					'We map point here',
					'PointMapVariable is ',
					SYS._str(self.PointMapVariable)
				]
			)

		#map
		map(
				lambda __ElementVariable:
				self.point(
					*__ElementVariable
				)
				if type(__ElementVariable) in [list,tuple]
				else self.point(
					__ElementVariable
				),
				self.PointMapVariable if type(
					self.PointMapVariable
				)==list else self.PointMapVariable.items()
			)

	"""
	def propertize_setWatchAfterParentWithParenterBool(self,_SettingValueVariable):

		#set the value of the "hidden" property variable
		self._WatchAfterParentWithParenterBool=_SettingValueVariable

		#mapPoint
		self.PointingBackBool=True
		self.mapPoint()
	"""

#</DefineClass>

#<DefineLocals>

#Define
"""
class InletsClass(.ParenterClass):
	ManagingValueClass=PointerClass
class OutletsClass(Parenter.ParenterClass):
	ManagingValueClass=PointerClass
"""

"""
class InletsClass(PointerClass):
	ManagingValueClass=PointerClass
class OutletsClass(PointerClass):
	ManagingValueClass=PointerClass
"""

"""
#Set
Teamer.TeamerClass.TeamingClassesDict={
	'Inlets':InletsClass,
	'Outlets':OutletsClass
}
"""

#Set
Teamer.TeamerClass.TeamingClassesDict={
	#'Inlets':InletsClass,
	#'Outlets':OutletsClass
	'Inlets':PointerClass,
	'Outlets':PointerClass
}

Manager.ManagerClass.ManagingValueClass=PointerClass
#</DefineLocals>

#</DefinePrint>
PointerClass.PrintingClassSkipKeyStrsList.extend(
	[
		#'PointToVariable',
		#'PointFromVariable',
		'PointingToGetVariable',
		'PointingToSetKeyVariable',
		'PointingBackSetKeyVariable',
		'PointingBackBool',
		'PointingManagementBool',
		'PointedToVariable'
	]
)
#<DefinePrint>
