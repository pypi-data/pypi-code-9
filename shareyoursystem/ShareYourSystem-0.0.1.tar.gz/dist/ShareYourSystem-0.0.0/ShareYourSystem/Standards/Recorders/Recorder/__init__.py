# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Recorder

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Viewers.Pyploter"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
SYS.addDo('Recorder','Record','Recording','Recorded')
#</DefineAugmentation>

#<ImportSpecificModules>
#</ImportSpecificModules>

#<DefineLocals>
RecordPrefixStr=""
#</DefineLocals>

#<DefineClass>
@DecorationClass(**{
	'ClassingStructureVariable':[
			('Trace','Traces'),
			('Sample','Samples')
		]
})
class RecorderClass(BaseClass):
	
	def default_init(self,
			_RecordKeyStr = "",
			_RecordingKeyVariable = None,
			_RecordingLabelVariable = None,
			_RecordingInitFloatsArray = None,
			_RecordingColorStr = "blue",
			_RecordingInitMeanVariable = None,
			_RecordingInitStdVariable = None,
			_RecordedTraceFloatsArray = None,
			_RecordedInitFloatsArray = None,
			_RecordedParentSingularStr = "",	
			_RecordedColorTuplesList = None,	
			**_KwargVariablesDict
		):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_record(
			self
		):	

		#/#################/#
		# Determine if it is an inside structure or the top
		#

		#debug
		'''
		self.debug(
			[
				'We record here',
				'First look for deeper teams in the structure',
			]
		)
		'''

		#Check
		if self.ParentedTotalSingularListDict!=None and len(self.ParentedTotalSingularListDict)>0:

			#debug
			'''
			self.debug(
				[
					'self.ParentedTotalSingularListDict.keys() is ',
					str(self.ParentedTotalSingularListDict.keys())
				]
			)
			'''

			#get
			self.RecordedParentSingularStr=self.ParentedTotalSingularListDict.keys()[0]

		#debug
		'''
		self.debug(
			[
				'Ok',
				('self.',self,['RecordedParentSingularStr'])
			]
		)
		'''

		#debug
		'''
		self.debug(
				[
					'We are at this level',
					('self.',self,['RecordedParentSingularStr'])
				]
			)
		'''
		
		#/###################/#
		# Cases
		#

		#Check
		if self.ParentDeriveTeamerVariable==None or 'Traces' in self.TeamDict or self.ParentDeriveTeamerVariable.TeamTagStr not in [
			'Traces',
			'Samples'
		]:

			#/###################/#
			# Recorder level
			# network

			#debug
			'''
			self.debug(
				[
					'This is the Recorder level',
					'we structure Traces and Samples'
				]
			)
			'''

			#structure
			self.structure(
				[
					'Traces',
					'Samples'
				],
				'#all',
				_ManagerCommandSetList=['record']
			)
			
		#Check
		else:

			#debug
			'''
			self.debug(
				[
					'Ok we check if this parentsingular has a special method ',
					('self.',self,[
						'RecordedParentSingularStr'
					])
				]
			)
			'''

			#set
			RecordedMethodKeyStr='record'+self.RecordedParentSingularStr

			#Check
			if hasattr(self,RecordedMethodKeyStr):

				#/########################/#
				# call the special record<RecordedParentSingularStr> method
				#

				#debug
				'''
				self.debug(
					[
						'It is a '+self.RecordedParentSingularStr+' level',
						'We record<RecordedParentSingularStr>'
					]
				)
				'''

				#call
				getattr(
					self,
					RecordedMethodKeyStr
				)()

				#debug
				'''
				self.debug(
					[
						'Ok we have setted record'+self.RecordedParentSingularStr
					]
				)
				'''	

	def recordTrace(self):
		
		#/###################/#
		# Traces level
		#

		#debug
		"""
		self.debug(
				[
					'This is the Traces level',
					'First get the array to trace',
					('self.',self,[
						'RecordingKeyVariable'
					])
				]
			)
		"""
		
		#get
		RecordedTopDeriveRecorderVariable=self.ParentDeriveTeamerVariable.ParentDeriveTeamerVariable

		#/##################/#
		# First get the array to trace
		#

		#get
		if type(self.RecordingKeyVariable)==None.__class__:

			#Check
			if RecordPrefixStr!="" and self.ManagementTagStr.startswith(RecordPrefixStr):

				#debug
				'''
				self.debug(
					[
						('self.',self,['ManagementTagStr']),
						'RecordedTopDeriveRecorderVariable is '+str(RecordedTopDeriveRecorderVariable)
					]
				)
				'''
				
				#get
				self.RecordedTraceFloatsArray=getattr(
					RecordedTopDeriveRecorderVariable,
					SYS.deprefix(
						self.ManagementTagStr,
						RecordPrefixStr
					)
				)

		elif type(self.RecordingKeyVariable).__name__!='ndarray':
	
			#get
			self.RecordedTraceFloatsArray=RecordedTopDeriveRecorderVariable[
				self.RecordingKeyVariable
			]

		else:

			#alias
			self.RecordedTraceFloatsArray=self.RecordingKeyVariable

			#alias
			if self.RecordKeyStr=="":
				self.RecordKeyStr=str(self.RecordingKeyVariable)

		#debug
		'''
		self.debug(
			[
				'We have getted the RecordedTraceFloatsArray',
				('self.',self,['RecordedTraceFloatsArray']),
				'Now set the init'
			]
		)
		'''

		#Check
		if type(self.RecordedTraceFloatsArray)!=None.__class__:

			#/##################/#
			# Prepare initial conditions
			# with the Matrixer

			#Check
			if type(self.RecordingInitFloatsArray)==None.__class__:

				#debug
				'''
				self.debug(
					[
						'We prepare the initial conditions',
						'len(self.RecordedTraceFloatsArray) is ',
						str(len(self.RecordedTraceFloatsArray)),
						('self.',self,[
								'NumscipyingStdFloat',
								'NumscipyingMeanFloat',
								'RecordedTraceFloatsArray'
							])
					]
				)
				'''
				
				#Check
				if self.RecordingInitStdVariable!=None:
			
					#set
					self.NumscipyingStdFloat=self.RecordingInitStdVariable

				elif RecordedTopDeriveRecorderVariable.RecordingInitStdVariable!=None:

					#set
					self.NumscipyingStdFloat=RecordedTopDeriveRecorderVariable.RecordingInitStdVariable

				#Check
				if self.RecordingInitMeanVariable!=None:
			
					#set
					self.NumscipyingMeanFloat=self.RecordingInitMeanVariable

				elif RecordedTopDeriveRecorderVariable.RecordingInitMeanVariable!=None:

					#set
					self.NumscipyingMeanFloat=RecordedTopDeriveRecorderVariable.RecordingInitMeanVariable



				#matrix
				self.RecordedInitFloatsArray=self.numscipy(
						_SizeTuple=(len(self.RecordedTraceFloatsArray),1),
						_StatBool=False
					).NumscipiedValueFloatsArray[:,0]

			else:

				#debug
				'''
				self.debug(
					[
						"we init with a fix array",
						('self.',self,[
								'RecordingInitFloatsArray'
							])
					]
				)
				'''
				
				#alias
				self.RecordedInitFloatsArray = self.RecordingInitFloatsArray

			#debug
			'''
			self.debug(
				[
					'We have prepared the initial conditions',
					('self.',self,[
						'RecordedInitFloatsArray'
					])
				]
			)
			'''
			
	def recordSample(self):

		#debug
		'''
		self.debug(
			[
				'This is the sample record level',
				('self.',self,[
					'RecordingLabelVariable'
				])
			]
		)
		'''

		#/##################/#
		# Build the colors
		#

		#Check
		if self.RecordingLabelVariable!=None:

			#get		
			self.RecordedColorTuplesList=SYS.getColorTuplesList(
				'black',
				self.RecordingColorStr,
				len(self.RecordingLabelVariable)+3,
				_PlotBool=False
			)[3:]

			#reverse
			self.RecordedColorTuplesList.reverse()

			#debug
			'''
			self.debug(
				[
					'We have setted the colors',
					('self.',self,[
						'RecordedColorTuplesList'
					])
				]
			)
			'''
			

	
#</DefineClass>

#</DefinePrint>
RecorderClass.PrintingClassSkipKeyStrsList.extend(
	[
		'RecordKeyStr',
		'RecordingKeyVariable',
		'RecordingLabelVariable',
		'RecordingInitFloatsArray',
		'RecordingColorStr',
		'RecordingInitMeanVariable',
		'RecordingInitStdVariable',
		'RecordedTraceFloatsArray',
		'RecordedInitFloatsArray',
		'RecordedParentSingularStr',
		'RecordedColorTuplesList'
	]
)
#<DefinePrint>
