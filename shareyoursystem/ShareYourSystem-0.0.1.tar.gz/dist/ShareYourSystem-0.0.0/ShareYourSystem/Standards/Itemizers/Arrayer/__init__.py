# -*- coding: utf-8 -*-
"""

<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


Arrayer instances

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Itemizers.Conditioner"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import itertools
#</ImportSpecificModules>

#<DefineLocals>
def getLiargVariablesList(_ValueVariable):
	return _ValueVariable
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class ArrayerClass(BaseClass):
	
	def default_init(self,
						_ArrayingKeyVariablesList=None,
						_ArrayingValueVariable=None,
						_ArrayingTopBool=True,
						**_KwargVariablesDict
					):

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_array(self):
		
		#debug
		'''
		self.debug(
				[
					'we array here',
					('self.',self,['ArrayingKeyVariablesList'])
				]
			)
		'''
		
		#Check
		if len(self.ArrayingKeyVariablesList)>0:

			
			#/####################/#
			# Is it going to be a set with several layers
			#

			#debug
			'''
			self.debug(
					[
						'Is it going to be a set with several layers ?',
						('self.',self,[
							'ArrayingKeyVariablesList',
							'ArrayingValueVariable'
						])
					]
				)
			'''

			#Check
			if SYS.getIsListsListBool(self.ArrayingKeyVariablesList):

				#debug
				'''
				self.debug(
					[
						'set with several layers',
						('self.',self,['ArrayingValueVariable'])
					]
				)
				'''

				#/####################/#
				# Adapt the shape of the ValueVariable
				#

				#list default
				ArrayedLocalValueVariablesList=[]
				ArrayedDeepValueVariable=[]

				#Check
				if self.ArrayingValueVariable!=None:

					#Check
					if len(
						self.ArrayingValueVariable
					)==1 and len(self.ArrayingKeyVariablesList[0])>1:

						#listify
						self.ArrayingValueVariable=[self.ArrayingValueVariable]

					#Check
					if type(self.ArrayingValueVariable)!=list:
						

						#debug
						'''
						self.debug(
							[
								'This is a total same setting',
								('self.',self,[
									'ArrayingKeyVariablesList',
									'ArrayingValueVariable'
								])
							]
						)
						'''
						
						#list
						ArrayedLocalValueVariablesList=[self.ArrayingValueVariable]*len(
							self.ArrayingKeyVariablesList[0]
						)
						ArrayedDeepValueVariable=self.ArrayingValueVariable

					elif len(self.ArrayingValueVariable)>0:

						#Check
						if SYS.getIsTuplesListBool(self.ArrayingValueVariable[0]) or hasattr(
							self.ArrayingValueVariable[0],'items'
						):

						 	#debug
						 	'''
						 	self.debug('This is an identical layered array setting')
						 	'''

						 	#list
						 	ArrayedLocalValueVariablesList=[self.ArrayingValueVariable[0]]*len(
						 		self.ArrayingKeyVariablesList
						 	)
						 	ArrayedDeepValueVariable=self.ArrayingValueVariable[1:]

						else:

							#debug
							'''
						 	self.debug('This is an original layered setting')
						 	'''

						 	#split
							ArrayedLocalValueVariablesList=self.ArrayingValueVariable[0]
							ArrayedDeepValueVariable=self.ArrayingValueVariable[1:]
				 	

				#debug
				'''
				self.debug(
					[
						'ArrayedLocalValueVariablesList is '+str(
							ArrayedLocalValueVariablesList),
						'ArrayedDeepValueVariable is '+str(
							ArrayedDeepValueVariable)
					]
				)
				'''

				#/####################/#
				# Case where we have to set and then array deeper
				#

				#Check
				if len(self.ArrayingKeyVariablesList)>1:

					#debug
					'''
					self.debug(
						[
							'self.ArrayingKeyVariablesList[0] is '+str(self.ArrayingKeyVariablesList[0]),
							'ArrayedLocalValueVariablesList is '+str(ArrayedLocalValueVariablesList),
							'first we set this layer'
						]
					)
					'''

					#map
					ArrayedGetValueVariablesList=map(
							lambda __ArrayingKeyVariable,__ArrayingLocalValueVariable:
							self.set(
									__ArrayingKeyVariable,
									__ArrayingLocalValueVariable
									if __ArrayingLocalValueVariable!=None
									else {}
								)[__ArrayingKeyVariable],
							self.ArrayingKeyVariablesList[0],
							ArrayedLocalValueVariablesList
						)

					#debug
					'''
					self.debug(
						[
							'Now we array further',
							'ArrayedDeepValueVariable'+str(ArrayedDeepValueVariable)
						]
					)
					'''
					
					#map the next array
					map(
							lambda __ArrayedGetValueVariable:
							__ArrayedGetValueVariable.array(
									self.ArrayingKeyVariablesList[1:],
									ArrayedDeepValueVariable
									if type(ArrayedDeepValueVariable)!=list or len(ArrayedDeepValueVariable)>0
									else None,
									False
								),
							ArrayedGetValueVariablesList
						)
					

				#/####################/#
				# Case where we have just to set
				#

				else:

					#debug
					'''
					self.debug(
							[
								'ArrayedLocalValueVariablesList is',
								str(ArrayedLocalValueVariablesList),
								('self.',self,['ArrayingKeyVariablesList'])
							]
						)
					'''
					
					#map
					map(
							lambda __ArrayingKeyVariable,__ArrayingLocalValueVariable:
							self.set(
									__ArrayingKeyVariable,
									__ArrayingLocalValueVariable
									if __ArrayingLocalValueVariable!=None
									else {}
								),
							self.ArrayingKeyVariablesList[0],
							ArrayedLocalValueVariablesList
						)

			#/####################/#
			# It is just one layer
			#

			else:

				#/####################/#
				# Adapt the shape of the ValueVariable
				#

				#list default
				ArrayedLocalValueVariablesList=[]

				#Check
				if self.ArrayingValueVariable==None:

					
					#just a map get
					self['#map@get'](*self.ArrayingKeyVariablesList)
				
				#Check
				elif type(self.ArrayingValueVariable)==list:

					#debug
					self.debug('This is an identical non layered setting')

					#map set
					self['#map@set'](
							zip(
								self.ArrayingKeyVariablesList,
								self.ArrayingValueVariable
							)
						)

				else:
	
					#map set
					self['#map@set'](
							zip(
								self.ArrayingKeyVariablesList,
								[self.ArrayingValueVariable]*len(self.ArrayingKeyVariablesList)
							)
						)

					#debug
					'''
					self.debug('This is an original non layered setting')
					'''
		

#</DefineClass>

#</DefinePrint>
ArrayerClass.PrintingClassSkipKeyStrsList.extend(
	[
		'ArrayingKeyVariablesList',
		'ArrayingValueVariable',
		'ArrayingTopBool'
	]
)
#<DefinePrint>

