# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Processer

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Interfacers.Filer"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import os
#</ImportSpecificModules>

#<DefineLocals>
ProcessFileStr="ProcessTemp"
ProcessPrefixStr="$"
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class ProcesserClass(BaseClass):
	
	def default_init(self,
						_ProcessingBashStr="",
						_ProcessingDirectStr=False,
						_ProcessingActionStr="open",
						_ProcessingTimeInt=1,
						_ProcessedBashStr="",
						_ProcessedPopenVariable=None,
						**_KwargVariablesDict
					):
		
		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)
			
	def do_process(self):

		#/##################/#
		# Check for open
		#
		

		#Check
		if self.ProcessingActionStr=='open':

			#import
			import subprocess

			if self.ProcessingDirectStr:

				#/##################/#
				# Direct case 
				#

				#popen
				self.ProcessedPopenVariable = subprocess.Popen(
						self.ProcessingBashStr.split(' '), 
						shell=False,
		               	stdout=subprocess.PIPE,
		               	stdin=subprocess.PIPE
		        )

			else:
				
				#/##################/#
				# Indirect case where we build a sh file and put in a text
				#

				#Define
				ProcessedBashPathStr=self.FolderingPathVariable+ProcessFileStr+'.txt'

				#Check
				if os.path.isfile(ProcessedBashPathStr):

					#debug
					'''
					self.debug('delete the previous')
					'''
					
					#rm
					os.popen('rm '+ProcessedBashPathStr)

				#set
				self.ProcessedBashStr='OUTPUT="$('+self.ProcessingBashStr+')"\n'
				self.ProcessedBashStr+='echo "${OUTPUT}" > '+ProcessedBashPathStr

				#debug
				'''
				self.debug(
						[
							'We write the sh bash script',
							('self.',self,['ProcessedBashStr'])
						]
					)
				'''

				#write
				self.file(
						ProcessFileStr+'.sh',
						'w',
						_WriteVariable=self.ProcessedBashStr
					).file(
						_ModeStr='c'
					)

				#debug
				'''
				self.debug(
					[
						'We call the supprocess',
						('self.',self,[
											'FiledPathStr',
										])
					]
				)
				'''

				#kill the previous maybe
				if self.ProcessedPopenVariable!=None:
					self.ProcessedPopenVariable.kill()

				#popen
				self.ProcessedPopenVariable = subprocess.Popen(
						[
							'sh',
							self.FiledPathStr,
						], 
						shell=False,
		               	stdout=subprocess.PIPE,
		               	stdin=subprocess.PIPE
		        )

				#debug
				'''
				self.debug(
					[
						'We read the output',
					]
				)
				'''

				#wait for connect
				import time
				ProcessedReadBool=False
				ProcessedCountInt=0
				while ProcessedReadBool==False and ProcessedCountInt<5:

					try:

						#read
						self.ProcessedBashStr=self.file(
									ProcessFileStr+'.txt',
									'r'
								).FiledReadVariable

						#set
						ProcessedReadBool=True

					except:

						#debug
						'''
						self.debug(
							[
								'File read not work'
							]
						)
						'''

						#say that it is not setted
						ProcessedReadBool=False
						ProcessedCountInt+=1
						time.sleep(0.2)

		#/##################/#
		# Check for kill
		#

		elif self.ProcessingActionStr=='kill':

			#kill the process
			if self.ProcessedPopenVariable!=None:

				#debug
				'''
				self.debug('kill the popen variable')
				'''
				
				#kill but before wait a bit to be sure that the db has time to refresh
				SYS.stdout('Kill the popen variable')
				SYS.wait(self.ProcessingTimeInt)
				self.ProcessedPopenVariable.kill()
				SYS.stdout('It is killed')

	def mimic_get(self):

		#Check
		if type(self.GettingKeyVariable)==str:

			#Check
			if self.GettingKeyVariable.startswith(ProcessPrefixStr):

				#deprefix
				GetProcessBashStr=SYS.deprefix(
						self.GettingKeyVariable,
						ProcessPrefixStr
					)

				#process
				self.process(
						GetProcessBashStr
					)

				#set
				self.GettedValueVariable=self.ProcessedBashStr

				#stop
				return {'HookingIsBool':False}

		#Cal the base method
		BaseClass.get(self)

#</DefineClass>

#</DefinePrint>
ProcesserClass.PrintingClassSkipKeyStrsList.extend(
	[
		'ProcessingBashStr',
		'ProcessedBashStr'
	]
)
#<DefinePrint>

#<DefineLocals>
def status(_ProcessStr,**_KwargVariablesDict):

	#Check
	if 'PythonSkipSelfBool' not in _KwargVariablesDict:
		PythonSkipSelfBool=False
	else:
		PythonSkipSelfBool=_KwargVariablesDict['PythonSkipSelfBool' ]

	#Debug
	'''
	print('Processer')
	print('_ProcessStr is '+_ProcessStr)
	print('')
	'''

	#call
	SnapshotStr=ProcesserClass(
		).process(
			"ps -ef | grep "+_ProcessStr,
			**{
				'FolderingPathVariable':SYS.Processer.LocalFolderPathStr
			}
		).ProcessedBashStr

	#Debug
	'''
	print('Processer')
	print('SnapshotStr is '+SnapshotStr)
	print('')
	'''

	#filter the grep command process
	LineStrsList=SYS._filter(
			lambda __LineStr:
			'grep' not in __LineStr,
			SnapshotStr.split('\n')
		)

	#map
	if _ProcessStr=='Python':

		#filter
		LineStrsList=SYS._filter(
				lambda __LineStr:
				SYS.PythonPathStr in __LineStr,
				LineStrsList
			)


	#debug
	'''
	print('Processer')
	print('LineStrsList is ')
	print(LineStrsList)
	print('')
	'''
	
	#filter
	LineStrsList=SYS._filter(
			lambda __LineStr:
			__LineStr!='',
			LineStrsList
		)

	#call
	IdStrsList=map(
		lambda __LineStr:
		__LineStr.split()[1],
		LineStrsList	
	)

	#Check
	if _ProcessStr=='Python' and PythonSkipSelfBool:

		#Check
		if len(IdStrsList)>0:
			IdStrsList=sorted(IdStrsList)[:-1]
		else:
			IdStrsList=[]

	#debug
	'''
	print('Processer')
	print('IdStrsList is ')
	print(IdStrsList)
	print('')
	'''

	#return
	return ' '.join(map(str,IdStrsList))

SYS.status=status
#</DefineLocals>

#</DefinePrint>
ProcesserClass.PrintingClassSkipKeyStrsList.extend(
	[
		'ProcessingBashStr',
		'ProcessingDirectStr',
		'ProcessingActionStr',
		'ProcessingTimeInt',
		'ProcessedBashStr',
		'ProcessedPopenVariable',
	]
)
#<DefinePrint>