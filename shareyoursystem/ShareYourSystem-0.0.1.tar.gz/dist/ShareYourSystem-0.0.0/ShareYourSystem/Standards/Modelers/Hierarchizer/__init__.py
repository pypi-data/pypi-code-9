# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Hierarchizer is a Joiner that taking care of the 
order of the joining connections between derived Joiners,
whatever is the level of their setting in the hierarchy of 
their parent derived Storers.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Modelers.Joiner"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
import tables
from ShareYourSystem.Standards.Noders import Noder
Joiner=BaseModule
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass(**{
	'ClassingSwitchMethodStrsList':[
		'model',
		'tabular',
		'join',
		'insert'
	]
})
class HierarchizerClass(BaseClass):
	
	#Definition
	RepresentingKeyStrsList=[
							]

	#@Hooker.HookerClass(**{'HookingAfterVariablesList':[{'CallingVariable':BaseClass.__init__}]})
	def default_init(self,
						**_KwargVariablesDict
					):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def mimic_insert(self):

		#debug
		'''
		self.debug(	
					[
						'we setSwitch first and insert',
						('self.',self,[
										'JoiningAttentionStr',
										'JoiningCollectionStr'
									])
					]
				)
		'''
		
		#<NotHook>
		#insert then
		BaseClass.insert(self)
		#</NotHook>

		#debug
		'''
		self.debug('we hierarchize now, self.hierarchize is '+str(self.hierarchize))
		'''

		#call
		self.hierarchize()

		#switch first
		self.transmit(
			[
				('setSwitch',{
								'LiargVariablesList':[],
								'KwargVariablesDict':
								{
									'_ClassVariable':'Hierarchizer',
									'_DoStrsList':['Insert']
								}
							})
			],
			[self.JoiningAttentionStr+self.JoiningCollectionStr],
			#Self is not switched (if not it is circular !)
			#False
		)

	def do_hierarchize(self):

		#debug
		'''
		self.debug(
					[
						'insert then in the joined attention databasers',
						('self.',self,['JoinedAttentionCollectionOrderedDict'])
					]
				)
		'''

		#map
		map(
				lambda __JoinedAttentionCollectionDeriveJoinerPointer:
				__JoinedAttentionCollectionDeriveJoinerPointer.CatchToPointVariable.insert(),
				self.JoinedAttentionCollectionOrderedDict.values()
			)
		

#</DefineClass>

