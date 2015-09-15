# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


The Doer defines instances that are going to decorate a big family of classes in this framework. 
Staying on the idea, that one module should associate
one class, now a decorated class by a Doer should have a NameStr that is 
a DoStr and express also method a method with the name <DoStr>[0].lower()+<DoStr>[1:]
All the attributes that are controlling this method process are <DoingStr><MiddleStr><TypeStr>
and all the ones resetted during the method are <DoneStr><MiddleStr><TypeStr>.
This helps a lot for defining a fisrt level of objects that are acting like input-output controllers.

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Classors.Defaultor"
DecorationModuleStr=BaseModuleStr
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import collections
import inspect
import six
Defaultor=BaseModule
#</ImportSpecificModules>

#<DefineLocals>
DoingAttributePrefixStr='_'
DoingWrapPrefixStr='do_'
DoingDecorationPrefixStr=""
DoingDecorationTagStr="superDo"
DoingDecorationSuffixStr="_"
#</DefineLocals>

#<DefineFunctions>
def callDo(_InstanceVariable):

	#Call the .DoMethodStr
	return getattr(
		_InstanceVariable,
		_InstanceVariable.__class__.DoMethodStr
	)()

def getDoing(_InstanceVariable,_DoClassVariable=None):

	#check
	DoClassesList=SYS.GetList(_DoClassVariable,SYS)
	if len(DoClassesList)==0:
		DoClassesList=_InstanceVariable.__class__.MroDoerClassesList

	#Debug
	"""
	print('l 83 Doer')
	print('DoClassesList is ',DoClassesList)
	print('')
	"""

	#return
	return collections.OrderedDict(
		SYS.sum(
			map(
				lambda __DoClass:
				zip(
					__DoClass.DoingAttributeVariablesOrderedDict.keys(),
				map(
						lambda __DoneKeyStr:
						getattr(_InstanceVariable,__DoneKeyStr),
						__DoClass.DoingAttributeVariablesOrderedDict.keys()
					)
				),
				DoClassesList
			)
		)
	)

def setDoing(_InstanceVariable,_DoClassVariable=None,**_KwargVariablesDict):

	#check
	DoClassesList=SYS.GetList(_DoClassVariable,SYS)
	if len(DoClassesList)==0:
		DoClassesList=_InstanceVariable.__class__.MroDoerClassesList
		
	#map
	map(
			lambda __DoClass:
			_InstanceVariable.setDefault(
				__DoClass,
				__DoClass.DoingAttributeVariablesOrderedDict.keys(),
				**dict(
					_KwargVariablesDict,
					**{'DefaultMutableBool':True}
				)
			),
			DoClassesList
		)
	
	#return
	return _InstanceVariable

def getDone(_InstanceVariable,_DoClassVariable=None):

	#check
	DoClassesList=SYS.GetList(_DoClassVariable,SYS)
	if len(DoClassesList)==0:
		DoClassesList=_InstanceVariable.__class__.MroDoerClassesList
		
	#Debug
	"""
	print('l 83 Doer')
	print('_DoClassVariable is ',_DoClassVariable)
	print('')
	"""

	#return
	return collections.OrderedDict(
		SYS.sum(
			map(
				lambda __DoClass:
				zip(
					__DoClass.DoneAttributeVariablesOrderedDict.keys(),
				map(
						lambda __DoneKeyStr:
						getattr(_InstanceVariable,__DoneKeyStr),
						__DoClass.DoneAttributeVariablesOrderedDict.keys()
					)
				),
				DoClassesList
			)
		)
	)

def setDone(_InstanceVariable,_DoClassVariable=None,**_KwargVariablesDict):

	#Debug
	'''
	print('l 137 Doer setDone before check')
	print('_DoClassVariable is ',_DoClassVariable)
	print('')
	'''

	#check
	DoClassesList=SYS.GetList(_DoClassVariable,SYS)
	if len(DoClassesList)==0:
		DoClassesList=_InstanceVariable.__class__.MroDoerClassesList
		

	#Debug
	"""
	print('l 153 Doer')
	print('_DoClassVariable is ',_DoClassVariable)
	print('')
	"""

	#map
	map(
			lambda __DoClass:
			_InstanceVariable.setDefault(
				__DoClass,
				__DoClass.DoneAttributeVariablesOrderedDict.keys(),
				**dict(
					_KwargVariablesDict,
					**{'DefaultMutableBool':True}
				)
			),
			DoClassesList
		)

	#return 
	return _InstanceVariable

def getDo(_InstanceVariable,_DoClassVariable=None):
	
	#call
	return collections.OrderedDict(
			_InstanceVariable.getDoing(_DoClassVariable),
			**_InstanceVariable.getDone(_DoClassVariable)
		)

def setDo(_InstanceVariable,_DoClassVariable=None,**_KwargVariablesDict):

	#set
	_InstanceVariable.setDoing(_DoClassVariable,**_KwargVariablesDict)
	_InstanceVariable.setDone(_DoClassVariable,**_KwargVariablesDict)

	#return
	return _InstanceVariable

def DefaultDoFunction(
	_InstanceVariable,
	*_LiargVariablesList,
	**_KwargVariablesDict
):

	#return
	return _InstanceVariable

def do(
		_InstanceVariable,
		*_LiargVariablesList,
		**_KwargVariablesDict
	):

	#/################/#
	# Prepare the call of the do method
	#

	#Define
	DoDecorationMethodStr=_KwargVariablesDict['DoDecorationMethodStr']
	DoMethodStr=DoDecorationMethodStr.split(
		DoingDecorationPrefixStr+DoingDecorationTagStr+DoingDecorationSuffixStr
	)[-1] if DoingDecorationSuffixStr in DoDecorationMethodStr else DoDecorationMethodStr
	DoStr=DoMethodStr[0].upper()+DoMethodStr[1:] if DoMethodStr[0]!="_" else DoMethodStr[0]+DoMethodStr[1].upper()+DoMethodStr[2:]
	DoingStr=DoStrToDoingStrOrderedDict[DoStr]
	DoClassStr=_KwargVariablesDict['DoClassStr']
	DoClass=getattr(SYS,DoClassStr)
	DoWrapMethodStr=DoingWrapPrefixStr+DoMethodStr
	DoWrapUnboundMethod=getattr(
								DoClass,
								DoWrapMethodStr
							)
	del _KwargVariablesDict['DoDecorationMethodStr']
	del _KwargVariablesDict['DoClassStr']

	#/################/#
	# Look in the Kwarg if there were specifications of doing attributes
	#

	#debug
	'''
	print('Doer l.219 inside of the function DoFunction')
	#print('InstanceVariable is ',_InstanceVariable)
	print('_LiargVariablesList is ',_LiargVariablesList)
	print('_KwargVariablesDict is ',_KwargVariablesDict)
	print('')
	'''

	#Definition of the DoKwargTuplesList
	DoKwargTuplesList=map(
		lambda __KwargTuple:
		(
			DoingStr+DoingAttributePrefixStr.join(
			__KwargTuple[0].split(DoingAttributePrefixStr)[1:]),
			__KwargTuple[1]
		) if __KwargTuple[0].startswith(DoingAttributePrefixStr)
		else __KwargTuple,
		_KwargVariablesDict.items()
	)

	#Debug
	'''
	print('Doer l 239 ')
	print('DoKwargTuplesList is')
	print(DoKwargTuplesList)
	print('')
	'''

	#Check
	if len(DoKwargTuplesList)>0:

		#group by
		[
			DoClass.DoTempAttributeItemTuplesList,
			DoClass.DoTempNotAttributeItemTupleItemsList
		]=SYS.groupby(
			lambda __DoKwargTuple:
			hasattr(_InstanceVariable,__DoKwargTuple[0]),
			DoKwargTuplesList
		)

		#set in the instance the corresponding kwarged arguments
		map(	
				lambda __DoTempAttributeItemTuple:
				#set direct explicit attributes
				_InstanceVariable.__setattr__(*__DoTempAttributeItemTuple),
				DoClass.DoTempAttributeItemTuplesList
			)

		#Define
		DoneKwargDict=dict(DoClass.DoTempNotAttributeItemTupleItemsList)

	else:

		#Define
		DoneKwargDict={}

	#/################/#
	# Set to default values the doing and done mutables 
	#

	#set
	_InstanceVariable.setDefaultMutable(
		DoClass,
		_AttributeKeyVariable=DoClass.DoingAttributeVariablesOrderedDict.keys(
			)+DoClass.DoneAttributeVariablesOrderedDict.keys()
	)

	#debug
	'''
	print('Doer l.274 we are going to call the DoWrapUnboundMethod')
	print('DoWrapUnboundMethod is ',DoWrapUnboundMethod)
	print('_LiargVariablesList is ',_LiargVariablesList)
	print('')
	'''
	
	#Return the call of the defined do method
	if len(DoneKwargDict)>0:
		return DoWrapUnboundMethod(
			_InstanceVariable,
			*_LiargVariablesList,
			**DoneKwargDict
		)
	else:
		return DoWrapUnboundMethod(
			_InstanceVariable,
			*_LiargVariablesList
		)
#</DefineFunctions>


#<DefineClass>
@DecorationClass()
class DoerClass(BaseClass):

	def default_init(self,
						_DoClass=None,
						_DoingGetBool=False,
						**_KwargVariablesDict
					):
	
		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def __call__(self,_Class):

		#debug
		'''
		print('Doer l.247 __call__ method')
		print('_Class is ',_Class)
		print('')
		'''

		#Call the parent init method
		BaseClass.__call__(self,_Class)

		#Do
		self.do(_Class)

		#Debug
		'''
		print('do is done')
		print('')
		'''

		#Return 
		return _Class

	def do(self,_Class):

		#set
		self.DoClass=_Class
		
		#debug
		'''
		print("Doer l.337 : self.DoClass is ",self.DoClass)
		print('')
		'''

		#alias
		DoClass=self.DoClass

		#Definition
		DoerStr=DoClass.NameStr
		DoStr=DoerStrToDoStrOrderedDict[DoerStr]
		DoMethodStr=DoStr[0].lower()+DoStr[1:] if DoStr[0]!='_' else '_'+DoStr[1].lower()+DoStr[2:]
		DoneStr=DoStrToDoneStrOrderedDict[DoStr]
		DoingStr=DoneStrToDoingStrOrderedDict[DoneStr]
		LocalVariablesDict=vars()

		#debug
		'''
		print('Doer l.275 : DoerStr is '+DoerStr)
		print('DoStr is '+DoStr)
		print('DoMethodStr is '+DoMethodStr)
		print('DoingStr is '+DoingStr)
		print('DoneStr is '+DoneStr)
		print('')
		'''
		
		#set 
		map(
				lambda __KeyStr:
				setattr(DoClass,__KeyStr,LocalVariablesDict[__KeyStr]),
				['DoerStr','DoStr','DoneStr','DoingStr','DoMethodStr']
			)
		
		#set a lists that will contain the tempory setting items during a call of the <do> method in the instance
		#DoClass.DoHistoryOrderedDict=collections.OrderedDict()

		#Check
		if hasattr(DoClass,'DefaultAttributeVariablesOrderedDict'):
			
			#Debug
			'''
			print('Doer l.383')
			print('DoClass.DefaultAttributesVariablesOrderedDict is ',_Class.DefaultAttributesVariablesOrderedDict)
			print('')
			'''

			#Check for doing and done keyStrs
			DoClass.DoneAttributeVariablesOrderedDict=collections.OrderedDict(
				SYS._filter(
				lambda __DefaultAttributeItemTuple:
				__DefaultAttributeItemTuple[0].startswith(DoneStr),
				DoClass.DefaultAttributeVariablesOrderedDict.items()
				)
			)
			DoClass.DoingAttributeVariablesOrderedDict=collections.OrderedDict(
				SYS._filter(
				lambda __DefaultAttributeItemTuple:
				__DefaultAttributeItemTuple[0].startswith(DoingStr),
				DoClass.DefaultAttributeVariablesOrderedDict.items()
				)
			)
			DoClass.DoingDeprefixAttributeStrsList=map(
					lambda __KeyStr:
					DoingAttributePrefixStr+SYS.deprefix(__KeyStr,DoingStr),
					DoClass.DoingAttributeVariablesOrderedDict.keys()
				)

			#Definition
			DoWrapMethodStr=DoingWrapPrefixStr+DoMethodStr

			#Debug
			'''
			print('Doer l.401')
			print('DoClass.DoneAttributeVariablesOrderedDict is ',DoClass.DoneAttributeVariablesOrderedDict)
			print('DoClass.DoingAttributeVariablesOrderedDict is ',DoClass.DoingAttributeVariablesOrderedDict)
			print('DoWrapMethodStr is ',DoWrapMethodStr)
			print('')
			'''
			
			#Check 
			if hasattr(DoClass,DoWrapMethodStr):

				#Debug
				'''
				print('There is a DoWrapMethod here already')
				print('')
				'''

				#Get
				DoWrapMethod=getattr(
						DoClass,
						DoWrapMethodStr
					)
			else:

				#Debug
				'''
				print('There is no DoWrapMethod here')
				print('')
				'''

				#Definition of a default function
				DoWrapMethod = DefaultDoFunction

				#set
				setattr(DoClass,DoWrapMethodStr,DoWrapMethod)


			#debug
			'''
			print('DoWrapMethod is '+str(DoWrapMethod))
			print('')
			'''

			#Link
			"""
			DoingMethodKeyStr='init'+DoClass.NameStr
			setattr(
					DoClass,
					DoingMethodKeyStr,
					initDo
				)
			"""

			#/#################/#
			# Define the shape of the args
			#

			#Definition of the ExecStr that will define the function
			DoDecorationMethodStr=DoingDecorationPrefixStr+DoingDecorationTagStr+DoingDecorationSuffixStr+DoMethodStr
			DoExecStr="def "+DoDecorationMethodStr+"(_InstanceVariable,"
			DoExecStr+=",".join(
				map(
					lambda __DoingDeprefixAttributeStr:
					#DoingAttributePrefixStr+__KeyStr+"=None",
					__DoingDeprefixAttributeStr+"=None",
					#DoClass.DoingAttributeVariablesOrderedDict.keys()
					DoClass.DoingDeprefixAttributeStrsList
				)
			)
			DoExecStr+="," if DoExecStr[-1]!="," else ""
			DoExecStr+="*_LiargVariablesList,"
			DoExecStr+="**_KwargVariablesDict):\n\t"

			#/#################/#
			# Set the doing variables
			#

			#Debug part
			#DoExecStr+='\n\tprint("In '+DoDecorationMethodStr+' with '+DoWrapMethod.__name__+' ") '
			'''
			DoExecStr+="\n\t#Debug"
			DoExecStr+=('\n\t'+';\n\t'.join(
									map(
										lambda __KeyStr:
										'print("In DoerFunction, '+DoingAttributePrefixStr+__KeyStr+' is ",'+DoingAttributePrefixStr+__KeyStr+')',
										_Class.DoingAttributeVariablesOrderedDict.keys()
									)
								)+";") if len(_Class.DoingAttributeVariablesOrderedDict.keys())>0 else ''
			DoExecStr+='\n\tprint("_LiargVariablesList is ",_LiargVariablesList);'
			DoExecStr+='\n\tprint("_KwargVariablesDict is ",_KwargVariablesDict);\n\t'
			'''

			#join
			DoExecStr+=("\n"+";\n".join(
				map(
					lambda __KeyStr,__DoingDeprefixAttributeStr:
					"\n".join(
						[
							#"\tif type("+DoingAttributePrefixStr+__KeyStr+")!=None.__class__:",
							#"\t\t_InstanceVariable."+__KeyStr+"="+DoingAttributePrefixStr+__KeyStr,
							"\tif type("+__DoingDeprefixAttributeStr+")!=None.__class__:",
							"\t\t_InstanceVariable."+__KeyStr+"="+__DoingDeprefixAttributeStr,
						]
					),
					DoClass.DoingAttributeVariablesOrderedDict.keys(),
					DoClass.DoingDeprefixAttributeStrsList
				)
			)+";\n") if len(
				DoClass.DoingAttributeVariablesOrderedDict.keys()
			)>0 else ''

			#Give to the class this part (it can serve after for imitating methods...)
			DoExecStrKeyStr='Do'+DoClass.NameStr+'ExecStr'
			setattr(DoClass,DoExecStrKeyStr,DoExecStr)
			
			#Call the initDo method
			DoExecStr+="\n" if DoExecStr[-1]!="\n" else ""
			DoExecStr+="\n\t#return\n\t"
			
			#Check
			setattr(DoClass,'DoingGetBool',self.DoingGetBool)
			if self.DoingGetBool==False:

				#Return the _InstanceVariable if it is not a getter object
				DoExecStr+="do(_InstanceVariable,"
				DoExecStr+="*_LiargVariablesList,"
				DoExecStr+="**dict(_KwargVariablesDict,**{'DoDecorationMethodStr':'"+DoDecorationMethodStr+"','DoClassStr':'"+DoClass.__name__+"'}))\n\t"
				DoExecStr+="return _InstanceVariable\n"
			else:

				#Return the output of the do method
				DoExecStr+="return do(_InstanceVariable,"
				DoExecStr+="*_LiargVariablesList,"
				DoExecStr+="**dict(_KwargVariablesDict,**{'DoDecorationMethodStr':'"+DoDecorationMethodStr+"','DoClassStr':'"+DoClass.__name__+"'}))\n"

			#Debug
			'''
			print('Doer l 546')
			print('DoExecStr is ')
			print(DoExecStr)
			print('')
			'''
			
			#exec
			six.exec_(DoExecStr)

			#set
			#locals(
			#	)[DoDecorationMethodStr].DoWrapMethod=DoWrapMethod


			#Debug
			'''
			print('l. 907 Doer')
			print('DoClass is ',DoClass)
			print('DoDecorationMethodStr is ',DoDecorationMethodStr)
			print('DoWrapMethod is ',DoWrapMethod)
			print("locals()[DoDecorationMethodStr] is ",locals()[DoDecorationMethodStr])
			print('')
			'''
			
			#set with the specific name
			self.setMethod(DoDecorationMethodStr,locals()[DoDecorationMethodStr])

			#set with the DoMethodStr shortcut
			self.setMethod(DoMethodStr,locals()[DoDecorationMethodStr])

			#set a pointer to the fundamental class
			locals()[DoDecorationMethodStr].BaseDoClass=DoClass

			#/####################/#
			# Set maybe if not already the setDo methods
			#

			#Check
			if hasattr(DoClass,'setDo')==False:

				#Debug
				'''
				print('Doer l 602')
				print('DoClass is')
				print(DoClass)
				print('')
				'''
				
				#map
				map(
					lambda __SetUnboundMethod:
					#set with the DoMethodStr shortcut
					self.setMethod(
								__SetUnboundMethod.__name__,
								__SetUnboundMethod
							),
					[
						getDo,getDoing,getDone,
						setDo,setDoing,setDone,
						callDo
					]
				)

			#/####################/#
			# Give a list of all the mro Doer and the do possible
			#

			#set a DoMethodStrsList
			if hasattr(DoClass.__bases__[0],'MroDoerClassesList'):
				DoClass.MroDoerClassesList=DoClass.__bases__[0
				].MroDoerClassesList+[DoClass]
			else:
				DoClass.MroDoerClassesList=[DoClass]

			#set a DoMethodStrsList
			if hasattr(DoClass.__bases__[0],'DoMethodStrsList'):
				DoClass.DoMethodStrsList=DoClass.__bases__[0
				].DoMethodStrsList+[DoMethodStr]
			else:
				DoClass.DoMethodStrsList=[DoMethodStr]


		#Check
		DoClass.DoUnitsInt=-1

		#Add to the KeyStrsList
		DoClass.KeyStrsList+=[
								'DoerStr',
								'DoStr',
								'DoneStr',
								'DoingStr',
								'DoneAttributeVariablesOrderedDict',
								'DoingAttributeVariablesOrderedDict',
								'DoingDeprefixAttributeStrsList',
								'DoMethodStr',
								'DoHistoryOrderedDict',
								DoExecStrKeyStr,
								'DoingGetBool',
								'DoTempAttributeItemTuplesList',
								'DoTempNotAttributeItemTupleItemsList',
								'DoMethodStrsList',
								'MroDoerClassesList',
								'DoUnitsInt'
						]
						#No need to add the doing and done keys because they are already in the defaults keys
						#+DoClass.DoingAttributeVariablesOrderedDict.keys(
						#	)+DoClass.DoneAttributeVariablesOrderedDict.keys()
#</DefineClass>


#<DefineLocals>
DoStrsTuplesList=[
	('Doer','Do','Doing','Done'),
	('Deriver','Derive','Deriving','Derived'),
	('Propertiser','Propertize','Propertizing','Propertized'),
	('Inspecter','Inspect','Inspecting','Inspected'),
	('Representer','Represent','Representing','Represented'),
	('Debugger','Debug','Debugging','Debugged'),
	('Functer','Funct','Functing','Functed'),
	('Moduler','Module','Moduling','Moduled'),
	('Attester','Attest','Attesting','Attested'),
	('Tester','Test','Testing','Tested'),
	('Hooker','Hook','Hooking','Hooked'),
	('Conditioner','Condition','Conditioning','Conditioned'),
	('Concluder','Conclude','Concluding','Concluded'),
	('Observer','Observe','Observing','Observed'),
	('Binder','Bind','Binding','Binded'),
	('Switcher','Switch','Switching','Switched'),
	('Resetter','Reset','Resetting','Resetted'),
	('Caller','Call','Calling','Called'),
	('Cloner','Clone','Cloning','Cloned'),
	('Watcher','Watch','Watching','Watched'),
	('Classer','_Class','Classing','Classed'),
	('Argumenter','Argument','Argumenting','Argumented'),
	('Imitater','Imitate','Imitating','Imitated'),
	('Alerter','Alert','Alerting','Alerted'),
	('Interfacer','Interface','Interfacing','Interfaced'),
	('Folderer','Folder','Foldering','Foldered'),
	('Filer','File','Filing','Filed'),
	('Closer','Close','Closing','Closed'),
	('Loader','Load','Loading','Loaded'),
	('Writer','Write','Writing','Writed'),
	('Capturer','Capture','Capturing','Captured'),
	('Processer','Process','Processing','Processed'),
	('Statuser','Status','Statusing','Statused'),
	('Killer','Kill','Killing','Killed'),
	('Directer','Direct','Directing','Directed'),
	('Hdformater','Hdformat','Hdformating','Hdformated'),
	('Guider','Guide','Guiding','Guided'),
	('Scriptbooker','Scriptbook','Scriptbooking','Scriptbooked'),
	('Celler','Cell','Celling','Celled'),
	('Notebooker','Notebook','Notebooking','Notebooked'),
	('Markdowner','Markdown','Markdowning','Markdowned'),
	('Readmer','Readme','Readming','Readmed'),
	('Installer','Install','Installing','Installed'),
	('Documenter','Document','Documenting','Documented'),
	('Itemizer','Itemize','Itemizing','Itemized'),
	('Getter','Get','Getting','Getted'),
	('Setter','Set','Setting','Setted'),
	('Deleter','Delete','Deleting','Deleted'),
	('Attributer','Attribute','Attributing','Attributed'),
	('Restricter','Restrict','Restricting','Restricted'),
	('Pather','Path','Pathing','Pathed'),
	('Sharer','Share','Sharing','Shared'),
	('Executer','Execute','Executing','Executed'),
	('Pointer','Point','Pointing','Pointed'),
	('Applyier','Apply','Applying','Applied'),
	('Mapper','Map','Mapping','Mapped'),
	('Picker','Pick','Picking','Pick'),
	('Gatherer','Gather','Gathering','Gathered'),
	('Updater','Update','Updating','Updated'),
	('Linker','Link','Linking','Linked'),
	('Weaver','Weave','Weaving','Weaved'),
	('Filterer','Filter','Filtering','Filterer'),
	('Cooper','Coop','Cooping','Cooped'),
	('Familiarizer','Familiarize','Familiarizing','Familiarized'),
	('Teamer','Team','Teaming','Teamed'),
	('Manager','Manage','Managing','Managed'),
	('Noder','Node','Noding','Noded'),
	('Outputer','Output','Outputing','Outputed'),
	('Appender','Append','Appending','Appended'),
	('Instancer','Instance','Instancing','Instanced'),
	('Adder','Add','Adding','Added'),
	('Distinguisher','Distinguish','Distinguishing','Distinguished'),
	('Parenter','Parent','Parenting','Parented'),
	('Storer','Store','Storing','Stored'),
	('Pusher','Push','Pushing','Pushed'),
	('Producer','Produce','Producing','Produced'),
	('Catcher','Catch','Catching','Catched'),
	('Attentioner','Attention','Attentioning','Attentioned'),
	('Coupler','Couple','Coupling','Coupled'),
	('Settler','Settle','Settling','Settled'),
	('Commander','Command','Commanding','Commanded'),
	('Walker','Walk','Walking','Walked'),
	('Collecter','Collect','Collecting','Collected'),
	('Visiter','Visit','Visiting','Visited'),
	('Recruiter','Recruit','Recruiting','Recruit'),
	('Mobilizer','Mobilize','Mobilizing','Mobilized'),
	('Router','Route','Routing','Routed'),
	('Grabber','Grab','Grabbing','Grabbed'),
	('Poker','Poke','Poking','Poked'),
	('Connecter','Connect','Connecting','Connected'),
	('Networker','Network','Networking','Networked'),
	('Grouper','Group','Grouping','Grouped'),
	('Structurer','Structure','Structuring','Structured'),
	('Saver','Save','Saving','Saved'),
	('Databaser','Database','Modeling','Modeled'),
	('Modeler','Model','Modeling','Modeled'),
	('Tabularer','Tabular','Tabularing','Tabulared'),
	('Tabler','Table','Tabling','Tabled'),
	('Rower','Row','Rowing','Rowed'),
	('Inserter','Insert','Inserting','Inserted'),
	('Retriever','Retrieve','Retrieving','Retrieved'),
	('Findoer','Find','Finding','Found'),
	('Recoverer','Recover','Recovering','Recovered'),
	('Shaper','Shape','Shaping','Shaped'),
	('Merger','Merge','Merging','Merged'),
	('Scanner','Scan','Scanning','Scanned'),
	('Joiner','Join','Joining','Joined'),
	('Hierarchizer','Hierarchize','Hierarchizing','Hierarchized'),
	('Analyzer','Analyze','Analyzing','Analyzed'),
	('Grider','Grid','Griding','Grided'),
	('Controller','Control','Controlling','Controlled'),
	('Featurer','Feature','Featuring','Featured'),
	('Recuperater','Recuperate','Recuperating','Recuperated'),
	('Ploter','Plot','Ploting','Ploted'),
	('Axer','Axe','Axing','Axed'),
	('Paneler','Panel','Paneling','Paneled'),
	('Figurer','Figure','Figuring','Figured'),
	('Pyploter','Pyplot','Pyploting','Pyploted'),
	('Multiplier','Multiply','Multiplying','Multiplied'),
	('Sumer','Sum','Suming','Sumed'),
	('Modulizer','Modulize','Modulizing','Modulized'),
	('Simulater','Simulate','Simulating','Simulated'),
	('Runner','Run','Running','Runned'),
	('Moniter','Monit','Monitering','Monitered'),
	('Populater','Populate','Populating','Populated'),
	('Dynamizer','Dynamize','Dynamizing','Dynamized'),
	('Rater','Rate','Rating','Rated'),
	('Brianer','Brian','Brianing','Brianed'),
	('Muziker','Muzik','Muziking','Muziked'),
	('Vexflower','Vexflow','Vexflowing','Vexflowed'),
	('Permuter','Permute','Permuting','Permuted'),
	('Differenciater','Differenciate','Differenciating','Differenciated'),
	('Pooler','Pool','Pooling','Pooled'),
	('Harmonizer','Harmonize','Harmozing','Harmonized'),
	('Maker','Make','Making','Made'),
	('Builder','Build','Building','Built'),
	('Incrementer','Increment','Incrementing','Incremented'),
	('Mimicker','Mimic','Mimicking','Mimicked'),
	('Blocker','Block','Blocking','Blocked'),
	('Cumulater','Cumulate','Cumulating','Cumulated'),
	('Rebooter','Reboot','Rebooting','Rebooted'),
	('Triggerer','Trigger','Triggering','Triggered'),
	('Decrementer','Decrement','Decrementing','Decremented'),
	('Nbconverter','Nbconvert','Nbconverting','Nbconverted'),
	('Documenter','Document','Documenting','Documented'),
	('Packager','Package','Packaging','Packaged'),
	('Deployer','Deploy','Deploying','Deployed'),
	('Transmitter','Transmit','Transmitting','Transmitted'),
	('Factorizer','Factorize','Factorizing','Factorized'),
	('Organizer','Organize','Organizing','Organized'),
	('Neuroner','Neuron','Neuroning','Neuroned'),
	('Neurongrouper','Neurongroup','Neurongrouping','Neurongrouped'),
	('Lifer','Lif','Lifing','Lifed'),
	('Synapser','Synapse','Synapsing','Synapsed'),
	('Grasper','Grasp','Grasping','Grasped'),
	('Meteorer','Meteor','Meteoring','Meteored'),
	('Viewer','View','Viewing','Viewed'),
	('Boxer','Box','Boxing','Boxed'),
	('Consoler','Console','Consoling','Consoled'),
	('Systemer','System','Systeming','Systemed'),
	('Patcher','Patch','Patching','Patched'),
	('Arrayer','Array','Arraying','Arrayed'),
	('Matrixer','Matrix','Matrixing','Matrixed'),
	('Eulerer','Euler','Eulering','Eulered'),
	('Integrater','Integrate','Integrating','Integrated'),
	('Pydelayer','Pydelay','Pydelaying','Pydelayed'),
	('Equationer','Equation','Equationing','Equationed'),
	('Scaler','Scale','Scaling','Scaled'),
	('Streamer','Stream','Streaming','Streamed'),
	('Predicter','Predict','Predicting','Predicted'),
	('Predispiker','Predispike','Predispiking','Predispiked'),
	('Predirater','Predirate','Predirating','Predirated'),
	('Leaker','Leak','Leaking','Leaked'),
	('Expresser','Express','Expressing','Expressed'),
	('Pymongoer','Pymongo','Pymongoing','Pymongone'),
	('Texter','Text','Texting','Texted')
]
DoerStrToDoStrOrderedDict=SYS.dictify(DoStrsTuplesList,0,1)
DoStrToDoerStrOrderedDict=SYS.dictify(DoStrsTuplesList,1,0)
DoStrToDoingStrOrderedDict=SYS.dictify(DoStrsTuplesList,1,2)
DoStrToDoneStrOrderedDict=SYS.dictify(DoStrsTuplesList,1,3)
DoneStrToDoingStrOrderedDict=SYS.dictify(DoStrsTuplesList,3,2)

def addDo(*_DoStrsTuple):
	DoStrsTuplesList.append(_DoStrsTuple)
	DoerStrToDoStrOrderedDict[_DoStrsTuple[0]]=_DoStrsTuple[1]
	DoStrToDoerStrOrderedDict[_DoStrsTuple[1]]=_DoStrsTuple[0]
	DoStrToDoingStrOrderedDict[_DoStrsTuple[1]]=_DoStrsTuple[2]
	DoStrToDoneStrOrderedDict[_DoStrsTuple[1]]=_DoStrsTuple[3]
	DoneStrToDoingStrOrderedDict[_DoStrsTuple[3]]=_DoStrsTuple[2]
SYS.addDo=addDo

def setInitArray(_InstanceVariable,_DoStr,_TagStr):

	#get
	Variable=getattr(
		_InstanceVariable,
		DoStrToDoingStrOrderedDict[_DoStr]+_TagStr+'Variable'
	)

	#type
	Type=type(Variable)

	#import
	import numpy as np

	#Check
	if Type in [list,np.array]:

		#array
		setattr(
			_InstanceVariable,
			DoStrToDoneStrOrderedDict[_DoStr]+_TagStr+'Variable',
			np.array(
				Variable
			)
		)

	else:

		#array
		setattr(
			_InstanceVariable,
			DoStrToDoneStrOrderedDict[_DoStr]+_TagStr+'Variable',	
			Variable
		)
SYS.setInitArray=setInitArray

def setInitList(_InstanceVariable,_DoStr,_TagStr):

	#get
	Variable=getattr(
		_InstanceVariable,
		DoStrToDoingStrOrderedDict[_DoStr]+_TagStr+'Variable'
	)

	#type
	Type=type(Variable)

	#import
	import numpy as np

	#set
	SetKeyStr = DoStrToDoneStrOrderedDict[_DoStr]+_TagStr+'FloatsList'

	#Check
	if Type in [list,np.array]:

		#array
		setattr(
			_InstanceVariable,
			SetKeyStr,
			list(
				Variable
			)
		)

	else:

		#array
		setattr(
			_InstanceVariable,
			SetKeyStr,	
			[Variable]
		)

	#Check
	NewDoUnitsInt = len(getattr(_InstanceVariable,SetKeyStr))

	#Check
	if _InstanceVariable.DoUnitsInt<NewDoUnitsInt:
		_InstanceVariable.DoUnitsInt = NewDoUnitsInt

SYS.setInitList=setInitList
#</DefineLocals>

