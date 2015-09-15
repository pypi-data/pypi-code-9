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
BaseModuleStr="ShareYourSystem.Standards.Classors.Defaultor")
DecorationModule=BaseModule
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>

import collections
import inspect
import six
#</ImportSpecificModules>

#<DefineLocals>
DoingAttributePrefixStr='_'
#DoingDecorationPrefixStr='@'
DoingWrapPrefixStr='do_'
DoingDecorationPrefixStr=""
DoingDecorationTagStr="superDo"
DoingDecorationSuffixStr="_"
#</DefineLocals>

#<DefineFunctions>
def DefaultDoFunction(
	_InstanceVariable,
	*_LiargVariablesList,
	**_KwargVariablesDict
):
	return _InstanceVariable

def do(
				_InstanceVariable,
				*_LiargVariablesList,
				**_KwargVariablesDict
			):

	#Define
	DoDecorationMethodStr=_KwargVariablesDict['DoDecorationMethodStr']
	DoMethodStr=DoDecorationMethodStr.split(DoingDecorationSuffixStr)[-1] if DoingDecorationSuffixStr in DoDecorationMethodStr else DoDecorationMethodStr
	DoStr=DoMethodStr[0].upper()+DoMethodStr[1:]
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

	#debug
	'''
	print('Doer l.54 inside of the function DoFunction')
	print('InstanceVariable is ',_InstanceVariable)
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

	#map
	TypeClassesList=map(
			lambda __DoneKeyStr:
			SYS.getTypeClassWithTypeStr(
					SYS.getTypeStrWithKeyStr(__DoneKeyStr)
			)
			if getattr(_InstanceVariable,__DoneKeyStr)==None 
			else None.__class__,
			DoClass.DoingAttributeVariablesOrderedDict.keys(
				)+DoClass.DoneAttributeVariablesOrderedDict.keys()
	)

	#debug
	'''
	print('TypeClassesList is '+str(TypeClassesList))
	print('')
	'''

	#set in the instance
	map(
			lambda __DoneKeyStr,__TypeClass:
			setattr(
					_InstanceVariable,
					__DoneKeyStr,
					__TypeClass()
			)
			if __TypeClass!=None.__class__ 
			else None,
			DoClass.DoingAttributeVariablesOrderedDict.keys(
				)+DoClass.DoneAttributeVariablesOrderedDict.keys(),
			TypeClassesList
	)

	#debug
	'''
	print('Doer l.274 we are going to call the DoWrapMethod')
	print('DoWrapMethod is ',DoWrapMethod)
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
		print('Doer l.132 : DoerStr is '+DoerStr)
		print('DoStr is '+DoStr)
		print('DoMethodStr is '+DoMethodStr)
		print('DoingStr is '+DoingStr)
		print('DoneStr is '+DoneStr)
		print('')

		#set 
		map(
				lambda __KeyStr:
				setattr(DoClass,__KeyStr,LocalVariablesDict[__KeyStr]),
				['DoerStr','DoStr','DoneStr','DoingStr','DoMethodStr']
			)
		
		#set a lists that will contain the tempory setting items during a call of the <do> method in the instance
		DoClass.DoHistoryOrderedDict=collections.OrderedDict()

		#Check
		if hasattr(DoClass,'DefaultAttributeItemTuplesList'):
			
			#Debug
			'''
			print('Doer l.383')
			print('DoClass.DefaultAttributeItemTuplesList is ',_Class.DefaultAttributeItemTuplesList)
			print('')
			'''

			#Check for doing and done keyStrs
			DoClass.DoneAttributeVariablesOrderedDict=collections.OrderedDict(
				SYS._filter(
				lambda __DefaultAttributeItemTuple:
				__DefaultAttributeItemTuple[0].startswith(DoneStr),
				DoClass.DefaultAttributeItemTuplesList
				)
			)
			DoClass.DoingAttributeVariablesOrderedDict=collections.OrderedDict(
				SYS._filter(
				lambda __DefaultAttributeItemTuple:
				__DefaultAttributeItemTuple[0].startswith(DoingStr),
				DoClass.DefaultAttributeItemTuplesList
				)
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
				DoWrapMethod=DefaultDoFunction


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

			#Definition of the ExecStr that will define the function
			DoDecorationMethodStr=DoingDecorationPrefixStr+DoingDecorationTagStr+DoingDecorationSuffixStr+DoMethodStr
			DoExecStr="def "+DoDecorationMethodStr+"(_InstanceVariable,"
			DoExecStr+=",".join(
				map(
					lambda __KeyStr:
					DoingAttributePrefixStr+__KeyStr+"=None",
					DoClass.DoingAttributeVariablesOrderedDict.keys()
				)
			)
			DoExecStr+="," if DoExecStr[-1]!="," else ""
			DoExecStr+="*_LiargVariablesList,"
			DoExecStr+="**_KwargVariablesDict):\n\t"

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

			#Set the doing variables
			"""
			DoExecStr+="\n\t#set the doing variables"
			DoExecStr+="\n\tDoHistoryOrderedDict=_InstanceVariable.__class__.DoHistoryOrderedDict"
			DoExecStr+="\n\tif '"+DoDecorationMethodStr+"' not in DoHistoryOrderedDict:DoHistoryOrderedDict['"+DoDecorationMethodStr+"']=SYS.collections.OrderedDict()"
			DoExecStr+="\n\tDoneSpecificAttributesOrderedDict=DoHistoryOrderedDict['"+DoDecorationMethodStr+"']"
			DoExecStr+=("\n"+";\n".join(
			map(
				lambda __KeyStr:
				"\n".join(
					[
						"\tif "+DoingAttributePrefixStr+__KeyStr+"!=None:",
						"\t\t_InstanceVariable."+__KeyStr+"="+DoingAttributePrefixStr+__KeyStr,
						"\t\tDoneSpecificAttributesOrderedDict['"+__KeyStr+"']="+DoingAttributePrefixStr+__KeyStr,
						"\telse:",
						"\t\tDoneSpecificAttributesOrderedDict['"+__KeyStr+"']=None"
					]
				),
				DoClass.DoingAttributeVariablesOrderedDict.keys()
				)
			)+";\n") if len(
				DoClass.DoingAttributeVariablesOrderedDict.keys()
			)>0 else ''
			"""

			DoExecStr+=("\n"+";\n".join(
			map(
				lambda __KeyStr:
				"\n".join(
					[
						"\tif "+DoingAttributePrefixStr+__KeyStr+"!=None:",
						"\t\t_InstanceVariable."+__KeyStr+"="+DoingAttributePrefixStr+__KeyStr,
					]
				),
				DoClass.DoingAttributeVariablesOrderedDict.keys()
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
				DoExecStr+="return DoFunction(_InstanceVariable,"
				DoExecStr+="*_LiargVariablesList,"
				DoExecStr+="**dict(_KwargVariablesDict,**{'DoDecorationMethodStr':'"+DoDecorationMethodStr+"','DoClassStr':'"+DoClass.__name__+"'}))\n"

			#debug
			'''
			print('Doer l 403')
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
			setattr(
						DoClass,
						DoDecorationMethodStr,
						locals()[DoDecorationMethodStr]
					)

			#set with the DoMethodStr shortcut
			setattr(
						DoClass,
						DoMethodStr,
						locals()[DoDecorationMethodStr]
					)

		#Add to the KeyStrsList
		DoClass.KeyStrsList+=[
								'DoerStr',
								'DoStr',
								'DoneStr',
								'DoingStr',
								'DoneAttributeVariablesOrderedDict',
								'DoingAttributeVariablesOrderedDict',
								DoExecStrKeyStr,
								'DoingGetBool',
								'DoTempAttributeItemTuplesList',
								'DoTempNotAttributeItemTupleItemsList'
						]			
#</DefineClass>


#<DefineLocals>
DoStrsTuplesList=[
	('Doer','Do','Doing','Done'),
	('Deriver','Derive','Deriving','Derived'),
	('Propertiser','Propertize','Propertizing','Propertized'),
	('Inspecter','Inspect','Inspecting','Inspected'),
	('Representer','Represent','Representing','Represented'),
	('Printer','_Print','Printing','Printed'),
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
	('Cumulater','Cumulate','Cumulating','Cumulated')
]

DoerStrToDoStrOrderedDict=SYS.dictify(DoStrsTuplesList,0,1)
DoStrToDoerStrOrderedDict=SYS.dictify(DoStrsTuplesList,1,0)
DoStrToDoingStrOrderedDict=SYS.dictify(DoStrsTuplesList,1,2)
DoStrToDoneStrOrderedDict=SYS.dictify(DoStrsTuplesList,1,3)
DoneStrToDoingStrOrderedDict=SYS.dictify(DoStrsTuplesList,3,2)
#</DefineLocals>

