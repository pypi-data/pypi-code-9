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

#<DefineDoStrsList>
DoStrsList=["Doer","Do","Doing","Done"]
#<DefineDoStrsList>

#<DefineLocals>
DoingPrefixStr='_'
DoingDecorationStr='@'
DoingDoMethodStr='do_'
#</DefineLocals>

#<DefineFunctions>
def getDoerStrWithKeyStr(_KeyStr):

	#Check
	if len(_KeyStr)>0:

		#Split the Str into words
		WordStrsList=SYS.getWordStrsListWithStr(_KeyStr)
		if len(WordStrsList)>0:
			PrefixWordStr="".join(WordStrsList[:-1])
			LastWordStr=WordStrsList[-1]

			#debug
			'''
			print('Doer getDoerStrWithKeyStr')
			print('PrefixWordStr is '+str(PrefixWordStr))
			print('LastWordStr is '+str(LastWordStr))
			print('')
			'''

			if LastWordStr[0] in ["P","p"] and LastWordStr[1:]=="roperty":
				return PrefixWordStr+LastWordStr[0]+"ropertize"

		#Default return
		return _KeyStr+'er'

	#Return ""
	return ""

def getDoStrWithDoerStr(_DoerStr):

	#Check
	if len(_DoerStr)>0:

		#Split the Str into words
		WordStrsList=SYS.getWordStrsListWithStr(_DoerStr)
		if len(WordStrsList)>0:
			PrefixWordStr="".join(WordStrsList[:-1])
			LastWordStr=WordStrsList[-1]

			#debug
			'''
			print('Doer getDoStrWithDoerStr')
			print('PrefixWordStr is '+str(PrefixWordStr))
			print('LastWordStr is '+str(LastWordStr))
			print('')
			'''

			if LastWordStr[0] in ["A","a"] and LastWordStr[1:]=="pplyier":
				return PrefixWordStr+LastWordStr[0]+"pply"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="ultiplier":
				return PrefixWordStr+LastWordStr[0]+"ultiply"
			elif LastWordStr[0] in ["A","a"] and LastWordStr[1:]=="ttributer":
				return PrefixWordStr+LastWordStr[0]+"ttribute"
			elif LastWordStr[0] in ["A","a"] and LastWordStr[1:]=="nalyzer":
				return PrefixWordStr+LastWordStr[0]+"nalyze"
			elif LastWordStr[0] in ["I","i"] and LastWordStr[1:]=="nstancer":
				return PrefixWordStr+LastWordStr[0]+"nstance"
			elif LastWordStr[0] in ["C","c"] and LastWordStr[1:]=="oncluder":
				return PrefixWordStr+LastWordStr[0]+"onclude"
			elif LastWordStr[0] in ["N","n"] and LastWordStr[1:]=="oder":
				return PrefixWordStr+LastWordStr[0]+"ode"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="tructurer":
				return PrefixWordStr+LastWordStr[0]+"tructure"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="erger":
				return PrefixWordStr+LastWordStr[0]+"erge"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="unner":
				return PrefixWordStr+LastWordStr[0]+"un"
			elif LastWordStr[0] in ["D","d"] and LastWordStr[1:]=="ynamizer":
				return PrefixWordStr+LastWordStr[0]+"ynamize"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="obilizer":
				return PrefixWordStr+LastWordStr[0]+"obilize"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="ettler":
				return PrefixWordStr+LastWordStr[0]+"ettle"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="aver":
				return PrefixWordStr+LastWordStr[0]+"ave"
			elif LastWordStr[0] in ["D","d"] and LastWordStr[1:]=="atabaser":
				return PrefixWordStr+LastWordStr[0]+"atabase"
			elif LastWordStr[0] in ["F","f"] and LastWordStr[1:]=="indoer":
				return PrefixWordStr+LastWordStr[0]+"ind"
			elif LastWordStr[0] in ["P","p"] and LastWordStr[1:]=="roducer":
				return PrefixWordStr+LastWordStr[0]+"roduce"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="imulater":
				return PrefixWordStr+LastWordStr[0]+"imulate"
			elif LastWordStr[0] in ["C","c"] and LastWordStr[1:]=="apturer":
				return PrefixWordStr+LastWordStr[0]+"apture"
			elif LastWordStr[0] in ["C","c"] and LastWordStr[1:]=="loser":
				return PrefixWordStr+LastWordStr[0]+"lose"
			elif LastWordStr[0] in ["F","f"] and LastWordStr[1:]=="igurer":
				return PrefixWordStr+LastWordStr[0]+"igure"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="oniter":
				return PrefixWordStr+LastWordStr[0]+"onit"
			elif LastWordStr[0] in ["O","o"] and LastWordStr[1:]=="bserver":
				return PrefixWordStr+LastWordStr[0]+"bserve"
			elif LastWordStr[0] in ["P","p"] and LastWordStr[1:]=="opulater":
				return PrefixWordStr+LastWordStr[0]+"opulate"
			elif LastWordStr[0] in ["C","c"] and LastWordStr[1:]=="oupler":
				return PrefixWordStr+LastWordStr[0]+"ouple"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="canner":
				return PrefixWordStr+LastWordStr[0]+"can"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="etriever":
				return PrefixWordStr+LastWordStr[0]+"etrieve"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="haper":
				return PrefixWordStr+LastWordStr[0]+"hape"
			elif LastWordStr[0] in ["H","h"] and LastWordStr[1:]=="ierarchizer":
				return PrefixWordStr+LastWordStr[0]+"ierarchize"
			elif LastWordStr[0] in ["E","e"] and LastWordStr[1:]=="xecuter":
				return PrefixWordStr+LastWordStr[0]+"xecute"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="ecuperater":
				return PrefixWordStr+LastWordStr[0]+"ecuperate"
			elif LastWordStr[0] in ["C","c"] and LastWordStr[1:]=="loner":
				return PrefixWordStr+LastWordStr[0]+"lone"
			elif LastWordStr[0] in ["T","t"] and LastWordStr[1:]=="abler":
				return PrefixWordStr+LastWordStr[0]+"able"
			elif LastWordStr[0] in ["I","i"] and LastWordStr[1:]=="temizer":
				return PrefixWordStr+LastWordStr[0]+"temize"
			elif LastWordStr[0] in ["U","u"] and LastWordStr[1:]=="pdater":
				return PrefixWordStr+LastWordStr[0]+"pdate"
			elif LastWordStr[0] in ["C","c"] and LastWordStr[1:]=="oupler":
				return PrefixWordStr+LastWordStr[0]+"ouple"
			elif LastWordStr[0] in ["P","p"] and LastWordStr[1:]=="oker":
				return PrefixWordStr+LastWordStr[0]+"oke"
			elif LastWordStr[0] in ["G","g"] and LastWordStr[1:]=="uider":
				return PrefixWordStr+LastWordStr[0]+"uide"
			elif LastWordStr[0] in ["A","a"] and LastWordStr[1:]=="xer":
				return PrefixWordStr+LastWordStr[0]+"xe"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="ater":
				return PrefixWordStr+LastWordStr[0]+"ate"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="harer":
				return PrefixWordStr+LastWordStr[0]+"hare"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="esetter":
				return PrefixWordStr+LastWordStr[0]+"eset"
			elif LastWordStr[0] in ["W","w"] and LastWordStr[1:]=="riter":
				return PrefixWordStr+LastWordStr[0]+"rite"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="eadmer":
				return PrefixWordStr+LastWordStr[0]+"eadme"
			elif LastWordStr[0] in ["J","j"] and LastWordStr[1:]=="oiner":
				return PrefixWordStr+LastWordStr[0]+"oin"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="outer":
				return PrefixWordStr+LastWordStr[0]+"oute"
			elif LastWordStr[0] in ["W","w"] and LastWordStr[1:]=="eaver":
				return PrefixWordStr+LastWordStr[0]+"eave"
			elif LastWordStr[0] in ["D","d"] and LastWordStr[1:]=="ebugger":
				return PrefixWordStr+LastWordStr[0]+"ebug"
			elif LastWordStr[0] in ["D","d"] and LastWordStr[1:]=="eleter":
				return PrefixWordStr+LastWordStr[0]+"elete"
			elif LastWordStr[0] in ["I","i"] and LastWordStr[1:]=="mitater":
				return PrefixWordStr+LastWordStr[0]+"mitate"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="oduler":
				return PrefixWordStr+LastWordStr[0]+"odule"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="torer":
				return PrefixWordStr+LastWordStr[0]+"tore"
			elif LastWordStr[0] in ["F","f"] and LastWordStr[1:]=="iler":
				return PrefixWordStr+LastWordStr[0]+"ile"
			elif LastWordStr[0] in ["P","p"] and LastWordStr[1:]=="rinter":
				return '_'+PrefixWordStr+LastWordStr[0]+"rint"
			elif LastWordStr[0] in ["F","f"] and LastWordStr[1:]=="eaturer":
				return PrefixWordStr+LastWordStr[0]+"eature"
			elif LastWordStr[0] in ["D","d"] and LastWordStr[1:]=="eriver":
				return PrefixWordStr+LastWordStr[0]+"erive"
			elif LastWordStr[0] in ["G","g"] and LastWordStr[1:]=="rabber":
				return PrefixWordStr+LastWordStr[0]+"rab"
			elif LastWordStr[0] in ["F","f"] and LastWordStr[1:]=="lattener":
				return PrefixWordStr+LastWordStr[0]+"latten"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="odulizer":
				return PrefixWordStr+LastWordStr[0]+"odulize"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="aker":
				return PrefixWordStr+LastWordStr[0]+"ake"
			elif LastWordStr[0] in ["F","f"] and LastWordStr[1:]=="indor":
				return PrefixWordStr+LastWordStr[0]+"ind"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="apper":
				return PrefixWordStr+LastWordStr[0]+"ap"
			elif LastWordStr[0] in ["F","f"] and LastWordStr[1:]=="unctor":
				return PrefixWordStr+LastWordStr[0]+"unc"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="etter":
				return PrefixWordStr+LastWordStr[0]+"et"
			elif LastWordStr[0] in ["G","g"] and LastWordStr[1:]=="etter":
				return PrefixWordStr+LastWordStr[0]+"et"
			elif LastWordStr[0] in ["P","p"] and LastWordStr[1:]=="ropertiser":
				return PrefixWordStr+LastWordStr[0]+"ropertize"

		#Default return
		return _DoerStr[:-2]

	#Return ""
	return ""

def getDoerStrWithDoStr(_DoStr):

	#Check
	if len(_DoStr)>0:

		#Split the Str into words
		WordStrsList=SYS.getWordStrsListWithStr(_DoStr)
		if len(WordStrsList)>0:
			PrefixWordStr="".join(WordStrsList[:-1])
			LastWordStr=WordStrsList[-1]

			#debug
			'''
			print('Doer getDoerStrWithDoStr')
			print('PrefixWordStr is '+str(PrefixWordStr))
			print('LastWordStr is '+str(LastWordStr))
			print('')
			'''

			if LastWordStr[0] in ["A","a"] and LastWordStr[1:]=="pply":
				return PrefixWordStr+LastWordStr[0]+"pplyier"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="ultiply":
				return PrefixWordStr+LastWordStr[0]+"ultiplier"
			elif LastWordStr[0] in ["N","n"] and LastWordStr[1:]=="ode":
				return PrefixWordStr+LastWordStr[0]+"oder"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="ave":
				return PrefixWordStr+LastWordStr[0]+"aver"
			elif LastWordStr[0] in ["C","c"] and LastWordStr[1:]=="apture":
				return PrefixWordStr+LastWordStr[0]+"apturer"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="eset":
				return PrefixWordStr+LastWordStr[0]+"esetter"
			elif LastWordStr[0] in ["C","c"] and LastWordStr[1:]=="ouple":
				return PrefixWordStr+LastWordStr[0]+"oupler"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="cann":
				return PrefixWordStr+LastWordStr[0]+"canner"
			elif LastWordStr[0] in ["F","f"] and LastWordStr[1:]=="igure":
				return PrefixWordStr+LastWordStr[0]+"igurer"
			elif LastWordStr[0] in ["C","c"] and LastWordStr[1:]=="lose":
				return PrefixWordStr+LastWordStr[0]+"loser"
			elif LastWordStr[0] in ["P","p"] and LastWordStr[1:]=="oke":
				return PrefixWordStr+LastWordStr[0]+"oker"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="un":
				return PrefixWordStr+LastWordStr[0]+"unner"
			elif LastWordStr[0] in ["C","c"] and LastWordStr[1:]=="lone":
				return PrefixWordStr+LastWordStr[0]+"loner"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="onit":
				return PrefixWordStr+LastWordStr[0]+"oniter"
			elif LastWordStr[0] in ["P","p"] and LastWordStr[1:]=="roduce":
				return PrefixWordStr+LastWordStr[0]+"roducer"
			elif LastWordStr[0] in ["O","o"] and LastWordStr[1:]=="bserve":
				return PrefixWordStr+LastWordStr[0]+"bserver"
			elif LastWordStr[0] in ["I","i"] and LastWordStr[1:]=="nstance":
				return PrefixWordStr+LastWordStr[0]+"nstancer"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="obilize":
				return PrefixWordStr+LastWordStr[0]+"obilizer"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="hape":
				return PrefixWordStr+LastWordStr[0]+"haper"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="oute":
				return PrefixWordStr+LastWordStr[0]+"outer"
			elif LastWordStr[0] in ["I","i"] and LastWordStr[1:]=="temize":
				return PrefixWordStr+LastWordStr[0]+"temizer"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="imulate":
				return PrefixWordStr+LastWordStr[0]+"imulater"
			elif LastWordStr[0] in ["P","p"] and LastWordStr[1:]=="opulate":
				return PrefixWordStr+LastWordStr[0]+"opulater"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="etrieve":
				return PrefixWordStr+LastWordStr[0]+"etriever"
			elif LastWordStr[0] in ["D","d"] and LastWordStr[1:]=="ynamize":
				return PrefixWordStr+LastWordStr[0]+"ynamizer"
			elif LastWordStr[0] in ["G","g"] and LastWordStr[1:]=="uide":
				return PrefixWordStr+LastWordStr[0]+"uider"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="ate":
				return PrefixWordStr+LastWordStr[0]+"ater"
			elif LastWordStr[0] in ["C","c"] and LastWordStr[1:]=="ouple":
				return PrefixWordStr+LastWordStr[0]+"oupler"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="ettle":
				return PrefixWordStr+LastWordStr[0]+"ettler"
			elif LastWordStr[0] in ["A","a"] and LastWordStr[1:]=="xe":
				return PrefixWordStr+LastWordStr[0]+"xer"
			elif LastWordStr[0] in ["J","j"] and LastWordStr[1:]=="oin":
				return PrefixWordStr+LastWordStr[0]+"oiner"
			elif LastWordStr[0] in ["W","w"] and LastWordStr[1:]=="eave":
				return PrefixWordStr+LastWordStr[0]+"eaver"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="ecuperate":
				return PrefixWordStr+LastWordStr[0]+"ecuperater"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="erge":
				return PrefixWordStr+LastWordStr[0]+"erger"
			elif LastWordStr[0] in ["C","c"] and LastWordStr[1:]=="onclude":
				return PrefixWordStr+LastWordStr[0]+"oncluder"
			elif LastWordStr[0] in ["H","h"] and LastWordStr[1:]=="ierarchize":
				return PrefixWordStr+LastWordStr[0]+"ierarchizer"
			elif LastWordStr[0] in ["A","a"] and LastWordStr[1:]=="nalyze":
				return PrefixWordStr+LastWordStr[0]+"nalyzer"
			elif LastWordStr[0] in ["F","f"] and LastWordStr[1:]=="ind":
				return PrefixWordStr+LastWordStr[0]+"indoer"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="tore":
				return PrefixWordStr+LastWordStr[0]+"torer"
			elif LastWordStr[0] in ["F","f"] and LastWordStr[1:]=="eature":
				return PrefixWordStr+LastWordStr[0]+"eaturer"
			elif LastWordStr[0] in ["D","d"] and LastWordStr[1:]=="atabase":
				return PrefixWordStr+LastWordStr[0]+"atabaser"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="tructure":
				return PrefixWordStr+LastWordStr[0]+"tructurer"
			elif LastWordStr[0] in ["E","e"] and LastWordStr[1:]=="xecute":
				return PrefixWordStr+LastWordStr[0]+"xecuter"
			elif LastWordStr[0] in ["T","t"] and LastWordStr[1:]=="able":
				return PrefixWordStr+LastWordStr[0]+"abler"
			elif LastWordStr[0] in ["U","u"] and LastWordStr[1:]=="pdate":
				return PrefixWordStr+LastWordStr[0]+"pdater"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="odule":
				return PrefixWordStr+LastWordStr[0]+"oduler"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="eadme":
				return PrefixWordStr+LastWordStr[0]+"eadmer"
			elif LastWordStr[0] in ["A","a"] and LastWordStr[1:]=="ttribute":
				return PrefixWordStr+LastWordStr[0]+"ttributer"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="hare":
				return PrefixWordStr+LastWordStr[0]+"harer"
			elif LastWordStr[0] in ["I","i"] and LastWordStr[1:]=="mitate":
				return PrefixWordStr+LastWordStr[0]+"mitater"
			elif LastWordStr[0] in ["D","d"] and LastWordStr[1:]=="elete":
				return PrefixWordStr+LastWordStr[0]+"eleter"
			elif LastWordStr[0] in ["F","f"] and LastWordStr[1:]=="ile":
				return PrefixWordStr+LastWordStr[0]+"iler"
			elif LastWordStr[0] in ["D","d"] and LastWordStr[1:]=="ebug":
				return PrefixWordStr+LastWordStr[0]+"ebugger"
			elif LastWordStr[0]=='_' and LastWordStr[1] in ["P","p"
			] and LastWordStr[1:]=="rint":
				return '_'+PrefixWordStr+LastWordStr[1]+"rinter"
			elif LastWordStr[0] in ["G","g"] and LastWordStr[1:]=="rab":
				return PrefixWordStr+LastWordStr[0]+"rabber"
			elif LastWordStr[0] in ["D","d"] and LastWordStr[1:]=="erive":
				return PrefixWordStr+LastWordStr[0]+"eriver"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="odulize":
				return PrefixWordStr+LastWordStr[0]+"odulizer"
			elif LastWordStr[0] in ["F","f"] and LastWordStr[1:]=="latten":
				return PrefixWordStr+LastWordStr[0]+"lattener"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="ake":
				return PrefixWordStr+LastWordStr[0]+"aker"
			elif LastWordStr[0] in ["F","f"] and LastWordStr[1:]=="ind":
				return PrefixWordStr+LastWordStr[0]+"indor"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="ap":
				return PrefixWordStr+LastWordStr[0]+"apper"
			elif LastWordStr[0] in ["F","f"] and LastWordStr[1:]=="unc":
				return PrefixWordStr+LastWordStr[0]+"unctor"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="et":
				return PrefixWordStr+LastWordStr[0]+"etter"
			elif LastWordStr[0] in ["G","g"] and LastWordStr[1:]=="et":
				return PrefixWordStr+LastWordStr[0]+"etter"
			elif LastWordStr[0] in ["P","p"] and LastWordStr[1:]=="ropertize":
				return PrefixWordStr+LastWordStr[0]+"ropertiser"

		#Default return
		if _DoStr[-1]!='e':
			return _DoStr+'er'
		else:
			return _DoStr+'r'

	#Return ""
	return ""

def getDoneStrWithDoStr(_DoStr):

	#Check
	if len(_DoStr)>0:

		#Split the Str into words
		WordStrsList=SYS.getWordStrsListWithStr(_DoStr)
		if len(WordStrsList)>0:
			PrefixWordStr="".join(WordStrsList[:-1])
			LastWordStr=WordStrsList[-1]

			#debug
			'''
			print('Doer getDoneStrWithDoStr')
			print('PrefixWordStr is '+str(PrefixWordStr))
			print('LastWordStr is '+str(LastWordStr))
			print('')
			'''

			if LastWordStr[0] in ["A","a"] and LastWordStr[1:]=='pply':
				return PrefixWordStr+LastWordStr[0]+'pplied'
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="ultiply":
				return PrefixWordStr+LastWordStr[0]+"ultiplied"
			elif LastWordStr[0]=='_' and LastWordStr[1] in ["P","p"
			] and LastWordStr[1:]=="rint":
				return PrefixWordStr+LastWordStr[0]+"rinted"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="odulize":
				return PrefixWordStr+LastWordStr[0]+"odulized"
			elif LastWordStr[0] in ["T","t"] and LastWordStr[1:]=="able":
				return PrefixWordStr+LastWordStr[0]+"abled"
			elif LastWordStr[0] in ["C","c"] and LastWordStr[1:]=="lone":
				return PrefixWordStr+LastWordStr[0]+"loned"
			elif LastWordStr[0] in ["A","a"] and LastWordStr[1:]=="ttention":
				return PrefixWordStr+LastWordStr[0]+"ttentioned"
			elif LastWordStr[0] in ["O","o"] and LastWordStr[1:]=="bserve":
				return PrefixWordStr+LastWordStr[0]+"bserved"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="oute":
				return PrefixWordStr+LastWordStr[0]+"outed"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="eset":
				return PrefixWordStr+LastWordStr[0]+"esetted"
			elif LastWordStr[0] in ["C","c"] and LastWordStr[1:]=="apture":
				return PrefixWordStr+LastWordStr[0]+"aptured"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="ave":
				return PrefixWordStr+LastWordStr[0]+"aved"
			elif LastWordStr[0] in ["G","g"] and LastWordStr[1:]=="uide":
				return PrefixWordStr+LastWordStr[0]+"uided"
			elif LastWordStr[0] in ["F","f"] and LastWordStr[1:]=="igure":
				return PrefixWordStr+LastWordStr[0]+"igured"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="onit":
				return PrefixWordStr+LastWordStr[0]+"onitered"
			elif LastWordStr[0] in ["C","c"] and LastWordStr[1:]=="ouple":
				return PrefixWordStr+LastWordStr[0]+"oupled"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="un":
				return PrefixWordStr+LastWordStr[0]+"unned"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="obilize":
				return PrefixWordStr+LastWordStr[0]+"obilized"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="ecuperate":
				return PrefixWordStr+LastWordStr[0]+"ecuperated"
			elif LastWordStr[0] in ["W","w"] and LastWordStr[1:]=="eave":
				return PrefixWordStr+LastWordStr[0]+"eaved"
			elif LastWordStr[0] in ["F","f"] and LastWordStr[1:]=="eature":
				return PrefixWordStr+LastWordStr[0]+"eatured"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="ate":
				return PrefixWordStr+LastWordStr[0]+"ated"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="cann":
				return PrefixWordStr+LastWordStr[0]+"canner"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="hape":
				return PrefixWordStr+LastWordStr[0]+"haped"
			elif LastWordStr[0] in ["J","j"] and LastWordStr[1:]=="oin":
				return PrefixWordStr+LastWordStr[0]+"oined"
			elif LastWordStr[0] in ["H","h"] and LastWordStr[1:]=="ierarchize":
				return PrefixWordStr+LastWordStr[0]+"ierarchized"
			elif LastWordStr[0] in ["I","i"] and LastWordStr[1:]=="nstance":
				return PrefixWordStr+LastWordStr[0]+"nstanced"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="etrieve":
				return PrefixWordStr+LastWordStr[0]+"etrieved"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="tore":
				return PrefixWordStr+LastWordStr[0]+"tored"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="erge":
				return PrefixWordStr+LastWordStr[0]+"erged"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="ettle":
				return PrefixWordStr+LastWordStr[0]+"ettled"
			elif LastWordStr[0] in ["U","u"] and LastWordStr[1:]=="pdate":
				return PrefixWordStr+LastWordStr[0]+"pdated"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="tructure":
				return PrefixWordStr+LastWordStr[0]+"tructured"
			elif LastWordStr[0] in ["D","d"] and LastWordStr[1:]=="atabase":
				return PrefixWordStr+LastWordStr[0]+"atabased"
			elif LastWordStr[0] in ["A","a"] and LastWordStr[1:]=="nalyze":
				return PrefixWordStr+LastWordStr[0]+"nalyzed"
			elif LastWordStr[0] in ["E","e"] and LastWordStr[1:]=="xecute":
				return PrefixWordStr+LastWordStr[0]+"xecuted"
			elif LastWordStr[0] in ["N","n"] and LastWordStr[1:]=="ode":
				return PrefixWordStr+LastWordStr[0]+"oded"
			elif LastWordStr[0] in ["R","r"] and LastWordStr[1:]=="eadme":
				return PrefixWordStr+LastWordStr[0]+"eadmed"
			elif LastWordStr[0] in ["C","c"] and LastWordStr[1:]=="onclude":
				return PrefixWordStr+LastWordStr[0]+"oncluded"
			elif LastWordStr[0] in ["C","c"] and LastWordStr[1:]=="lose":
				return PrefixWordStr+LastWordStr[0]+"losed"
			elif LastWordStr[0] in ["S","s"] and LastWordStr[1:]=="hare":
				return PrefixWordStr+LastWordStr[0]+"hared"
			elif LastWordStr[0] in ["A","a"] and LastWordStr[1:]=="ttribute":
				return PrefixWordStr+LastWordStr[0]+"ttributed"
			elif LastWordStr[0] in ["F","f"] and LastWordStr[1:]=="ile":
				return PrefixWordStr+LastWordStr[0]+"iled"
			elif LastWordStr[0] in ["D","d"] and LastWordStr[1:]=="ebug":
				return PrefixWordStr+LastWordStr[0]+"ebugged"
			elif LastWordStr[0] in ["D","d"] and LastWordStr[1:]=="eleter":
				return PrefixWordStr+LastWordStr[0]+"elete"
			elif LastWordStr[0] in ["D","d"] and LastWordStr[1:]=="erive":
				return PrefixWordStr+LastWordStr[0]+"erived"
			elif LastWordStr[0] in ["G","g"] and LastWordStr[1:]=="rab":
				return PrefixWordStr+LastWordStr[0]+"rabbed"
			elif LastWordStr[0] in ["F","f"] and LastWordStr[1:]=="latten":
				return PrefixWordStr+LastWordStr[0]+"lattened"
			elif LastWordStr[0] in ["I","i"] and LastWordStr[1:]=='nit':
				return PrefixWordStr+LastWordStr[0]+'nitiated'
			elif LastWordStr[0] in ["B","b"] and LastWordStr[1:]=="rian":
				return PrefixWordStr+LastWordStr[0]+"rianed"
			elif LastWordStr[0] in ["C","c"] and LastWordStr[1:]=="ondition":
				return PrefixWordStr+LastWordStr[0]+"onditioned"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="ap":
				return PrefixWordStr+LastWordStr[0]+"apped"
			elif LastWordStr[0] in ["F","f"] and LastWordStr[1:]=='unc':
				return PrefixWordStr+LastWordStr[0]+'uncted'
			elif LastWordStr[0] in ['D','d']and LastWordStr[1:]=='o':
				return PrefixWordStr+LastWordStr[0]+'one'
			elif LastWordStr[0] in ['P','p'] and LastWordStr[1:]=='arameter':
				return PrefixWordStr+LastWordStr[0]+'arameterized'
			elif LastWordStr[0] in ['F','f'] and LastWordStr[1:]=='ind':
				return PrefixWordStr+LastWordStr[0]+'ound'
			elif LastWordStr[0] in ['M','m'] and LastWordStr[1:]=='ake':
				return PrefixWordStr+LastWordStr[0]+'ade'
			elif LastWordStr[0] in ['F','f'] and LastWordStr[1:]=='ind':
				return PrefixWordStr+LastWordStr[0]+'ound'
			elif LastWordStr[0] in ['S','s'] and LastWordStr[1:]=='et':
				return PrefixWordStr+LastWordStr[0]+'etted'
			elif LastWordStr[0] in ['G','g'] and LastWordStr[1:]=='et':
				return PrefixWordStr+LastWordStr[0]+'etted'

		#Default return
		if _DoStr[-1] in ['n']:
			return _DoStr+_DoStr[-1]+"ed"
		elif _DoStr[-1] not in ['e','y']:
			return _DoStr+"ed" 
		elif _DoStr[-1]=='y':
			return _DoStr[:-1]+'ied'  
		else:
			return _DoStr[:-1]+'ed'

	#Return ""
	return ""

def getDoingStrWithDoneStr(_DoneStr):

	#Check
	if len(_DoneStr)>0:

		#Split the Str into words
		WordStrsList=SYS.getWordStrsListWithStr(_DoneStr)
		if len(WordStrsList)>0:
			PrefixWordStr="".join(WordStrsList[:-1])
			LastWordStr=WordStrsList[-1]

			#debug
			'''
			print('Doer getDoingStrWithDoneStr')
			print('PrefixWordStr is '+str(PrefixWordStr))
			print('LastWordStr is '+str(LastWordStr))
			print('')
			'''

			if LastWordStr[0] in ['M','m'] and LastWordStr[1:]=='ade':
				return PrefixWordStr+LastWordStr[0]+'aking'
			elif LastWordStr[0] in ['F','f'] and LastWordStr[1:]=='ound':
				return PrefixWordStr+LastWordStr[0]+'inding'
			elif LastWordStr[0] in ["F","f"] and LastWordStr[1:]=="lattened":
				return PrefixWordStr+LastWordStr[0]+"lattening"
			elif LastWordStr[0] in ["D","d"] and LastWordStr[1:]=="erived":
				return PrefixWordStr+LastWordStr[0]+"eriving"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="ultiplied":
				return PrefixWordStr+LastWordStr[0]+"ultiplying"
			elif LastWordStr[0] in ["M","m"] and LastWordStr[1:]=="odulized":
				return PrefixWordStr+LastWordStr[0]+"odulizing"
			elif LastWordStr[0] in ["G","g"] and LastWordStr[1:]=="rabbed":
				return PrefixWordStr+LastWordStr[0]+"rabbing"

		#Default return
		return _DoneStr[:-2]+"ing" if _DoneStr[-3]!='i' else _DoneStr[:-3]+'ying'

	#Return ""
	return ""

def getDoStrWithDoneStr(_DoneStr):

	#Check
	if len(_DoneStr)>0:

		if _DoneStr=='Parameterized':
			return 'Parameter'
		elif _DoneStr=='Found':
			return 'Find'
		elif len(_DoneStr)>0:
			if _DoneStr[-3] in ['y']:
				return _DoneStr[:-3]+'y'
		elif _DoneStr in ['Structured']:
			return _DoneStr[:-1]

	#Return ""
	return ""
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
		DoStr=getDoStrWithDoerStr(DoerStr)
		DoMethodStr=DoStr[0].lower()+DoStr[1:] if DoStr[0]!='_' else '_'+DoStr[1].lower()+DoStr[2:]
		DoneStr=getDoneStrWithDoStr(DoStr if DoStr[0]!='_' else DoStr[1:])
		DoingStr=getDoingStrWithDoneStr(DoneStr)
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
				['DoerStr','DoStr','DoneStr','DoingStr']
			)
		
		#set a lists that will contain the tempory setting items during a call of the <do> method in the instance
		DoClass.DoneAttributesOrderedDict=collections.OrderedDict()
		DoClass.DoneNotAttributesOrderedDict=collections.OrderedDict()

		#Check
		if hasattr(DoClass,'DefaultAttributeItemTuplesList'):
			
			#Debug
			'''
			print('Doer l.383')
			print('DoClass.DefaultAttributeItemTuplesList is ',_Class.DefaultAttributeItemTuplesList)
			print('')
			'''

			#Check for doing and done keyStrs
			DoClass.DoneAttributeVariablesOrderedDict=collections.OrderedDict(SYS._filter(
													lambda __DefaultAttributeTuple:
													__DefaultAttributeTuple[0].startswith(DoneStr),
													DoClass.DefaultAttributeItemTuplesList
												))
			DoClass.DoingAttributeVariablesOrderedDict=collections.OrderedDict(SYS._filter(
													lambda __DefaultAttributeTuple:
													__DefaultAttributeTuple[0].startswith(DoingStr),
													DoClass.DefaultAttributeItemTuplesList
												))

			#Definition
			DoMethodKeyStr=DoingDoMethodStr+DoMethodStr

			#Debug
			'''
			print('Doer l.401')
			print('DoClass.DoneAttributeVariablesOrderedDict is ',DoClass.DoneAttributeVariablesOrderedDict)
			print('DoClass.DoingAttributeVariablesOrderedDict is ',DoClass.DoingAttributeVariablesOrderedDict)
			print('DoMethodKeyStr is ',DoMethodKeyStr)
			print('')
			'''
			
			#Check 
			if hasattr(DoClass,DoMethodKeyStr):

				#Debug
				'''
				print('There is a DoMethod here already')
				print('')
				'''

				#Get
				DoneUnboundFunction=getattr(
						DoClass,
						DoMethodKeyStr
					).im_func
			else:

				#Debug
				'''
				print('There is no DoMethod here')
				print('')
				'''

				#Define
				def DefaultDoneUnboundFunction(
					_InstanceVariable,
					*_LiargVariablesList,
					**_KwargVariablesDict
				):
					return _InstanceVariable

				#Definition of a default function
				DoneUnboundFunction=DefaultDoneUnboundFunction


			#debug
			'''
			print('DoneUnboundFunction is '+str(DoneUnboundFunction))
			print('')
			'''

			#Definition of an initiating method for the mutable done variables
			def initDo(_InstanceVariable,*_LiargVariablesList,**_KwargVariablesDict):

				#debug
				'''
				print('Doer l.393 inside of the function initDo')
				print('InstanceVariable is ',_InstanceVariable)
				print('_LiargVariablesList is ',_LiargVariablesList)
				print('_KwargVariablesDict is ',_KwargVariablesDict)
				print('')
				'''

				#Definition of the DoneKwargTuplesList
				DoneKwargTuplesList=map(
										lambda __KwargTuple:
										(
											DoingStr+DoingPrefixStr.join(
											__KwargTuple[0].split(DoingPrefixStr)[1:]),
											__KwargTuple[1]
										) if __KwargTuple[0].startswith(DoingPrefixStr)
										else __KwargTuple,
										_KwargVariablesDict.items()
									)

				#Check
				if len(DoneKwargTuplesList)>0:

					#group by
					[DoClass.DoneAttributeTuplesList,DoClass.DoneNotAttributeTupleItemsList]=SYS.groupby(
						lambda __AttributeTuple:
						hasattr(_InstanceVariable,__AttributeTuple[0]),
						DoneKwargTuplesList
					)

					#set in the instance the corresponding kwarged arguments
					map(	
							lambda __AttributeTuple:
							#set direct explicit attributes
							_InstanceVariable.__setattr__(*__AttributeTuple),
							DoClass.DoneAttributeTuplesList
						)

					#Define
					DoneKwargDict=dict(DoClass.DoneNotAttributeTupleItemsList)

				else:

					#Define
					DoneKwargDict={}

				#map
				TypeClassesList=map(
						lambda __DoneKeyStr:
						SYS.getTypeClassWithTypeStr(
								SYS.getTypeStrWithKeyStr(__DoneKeyStr)
						) if getattr(_InstanceVariable,__DoneKeyStr
						)==None else None.__class__,
						_Class.DoingAttributeVariablesOrderedDict.keys(
							)+_Class.DoneAttributeVariablesOrderedDict.keys()
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
						) if __TypeClass!=None.__class__ else None,
						DoClass.DoingAttributeVariablesOrderedDict.keys(
							)+DoClass.DoneAttributeVariablesOrderedDict.keys(),
						TypeClassesList
				)
				
				#debug
				'''
				print('Doer l.476 we are going to call the DoneUnboundFunction')
				print('DoneUnboundFunction is ',DoneUnboundFunction)
				print('')
				'''

				#Return the call of the defined do method
				if len(DoneKwargDict)>0:
					return DoneUnboundFunction(
						_InstanceVariable,
						*_LiargVariablesList,
						**DoneKwargDict
					)
				else:
					return DoneUnboundFunction(
						_InstanceVariable,
						*_LiargVariablesList
					)
				
			#Link
			DoingMethodKeyStr='init'+DoClass.NameStr
			setattr(DoClass,DoingMethodKeyStr,initDo)

			#Definition of the ExecStr that will define the function
			DoneExecStr="def DoerFunction(_InstanceVariable,"
			DoneExecStr+=",".join(
									map(
										lambda __KeyStr:
										DoingPrefixStr+__KeyStr+"=None",
										DoClass.DoingAttributeVariablesOrderedDict.keys()
									)
								)
			DoneExecStr+="," if DoneExecStr[-1]!="," else ""

			DoneExecStr+="*_LiargVariablesList,"
			DoneExecStr+="**_KwargVariablesDict):\n\t"

			#set in the DoneAttributeTuplesList


			#Debug part
			#DoneExecStr+='\n\tprint("In DoerFunction with DoneUnboundFunction '+str(DoneUnboundFunction)+' ") '
			'''
			DoneExecStr+="\n\t#Debug"
			DoneExecStr+=('\n\t'+';\n\t'.join(
									map(
										lambda __KeyStr:
										'print("In DoerFunction, '+DoingPrefixStr+__KeyStr+' is ",'+DoingPrefixStr+__KeyStr+')',
										_Class.DoingAttributeVariablesOrderedDict.keys()
									)
								)+";") if len(_Class.DoingAttributeVariablesOrderedDict.keys())>0 else ''
			DoneExecStr+='\n\tprint("In DoerFunction, _LiargVariablesList is ",_LiargVariablesList);'
			DoneExecStr+='\n\tprint("In DoerFunction, _KwargVariablesDict is ",_KwargVariablesDict);\n\t'
			'''

			#Set the doing variables
			DoneExecStr+="\n\t#set the doing variables"
			DoneExecStr+="\n\tDoneAttributesOrderedDict=_InstanceVariable.__class__.DoneAttributesOrderedDict"
			DoneExecStr+="\n\tif '"+DoMethodStr+"' not in DoneAttributesOrderedDict:DoneAttributesOrderedDict['"+DoMethodStr+"']=SYS.collections.OrderedDict()"
			DoneExecStr+="\n\tDoneSpecificAttributesOrderedDict=DoneAttributesOrderedDict['"+DoMethodStr+"']"
			DoneExecStr+=("\n"+";\n".join(
									map(
										lambda __KeyStr:
										"\n".join(
											[
												"\tif "+DoingPrefixStr+__KeyStr+"!=None:",
												"\t\t_InstanceVariable."+__KeyStr+"="+DoingPrefixStr+__KeyStr,
												"\t\tDoneSpecificAttributesOrderedDict['"+__KeyStr+"']="+DoingPrefixStr+__KeyStr,
												"\telse:",
												"\t\tDoneSpecificAttributesOrderedDict['"+__KeyStr+"']=None"
											]
										),
										DoClass.DoingAttributeVariablesOrderedDict.keys()
									)
								)+";\n") if len(
			DoClass.DoingAttributeVariablesOrderedDict.keys())>0 else ''

			#Give to the class this part (it can serve after for imitating methods...)
			DoneExecStrKeyStr=DoClass.NameStr+'DoneExecStr'
			setattr(DoClass,DoneExecStrKeyStr,DoneExecStr)
			
			#Call the initDo method
			DoneExecStr+="\n" if DoneExecStr[-1]!="\n" else ""
			DoneExecStr+="\n\t#return\n\t"
			
			#Check
			setattr(DoClass,'DoingGetBool',self.DoingGetBool)
			if self.DoingGetBool==False:

				#Return the _InstanceVariable if it is not a getter object
				DoneExecStr+="_InstanceVariable.init"+DoClass.NameStr+"("
				DoneExecStr+="*_LiargVariablesList,"
				DoneExecStr+="**_KwargVariablesDict);\n\t"
				DoneExecStr+="return _InstanceVariable\n"
			else:

				#Return the output of the do method
				DoneExecStr+="return _InstanceVariable."+DoingMethodKeyStr+"("
				DoneExecStr+="*_LiargVariablesList,"
				DoneExecStr+="**_KwargVariablesDict)\n"

			#debug
			'''
			print('DoneExecStr is ')
			print(DoneExecStr)
			print('')
			'''
			
			#exec
			six.exec_(DoneExecStr)

			#set the name
			locals(
				)['DoerFunction'
			].__name__='DoerFunction'+DoingDecorationStr+DoMethodStr+' with DoneUnboundFunction '+str(DoneUnboundFunction)

			locals(
				)['DoerFunction'
			].DoneUnboundFunction=DoneUnboundFunction


			#Debug
			'''
			print('l. 907 Doer')
			print('DoClass is ',DoClass)
			print('DoMethodStr is ',DoMethodStr)
			print('DoneUnboundFunction is ',DoneUnboundFunction)
			print("locals()['DoerFunction'] is ",locals()['DoerFunction'])
			print('')
			'''
			
			#set a specific name
			setattr(DoClass,DoMethodStr,locals()['DoerFunction'])

			#set a unspecific do method
			setattr(DoClass,'setDoneVariables',locals()['DoerFunction'])


		#Add to the KeyStrsList
		DoClass.KeyStrsList+=[
										'DoerStr',
										'DoStr',
										'DoneStr',
										'DoingStr',
										'DoneAttributeVariablesOrderedDict',
										'DoingAttributeVariablesOrderedDict',
										DoneExecStrKeyStr,
										'DoingGetBool',
										'DoneAttributeTuplesList',
										'DoneNotAttributeTupleItemsList'
								]			
#</DefineClass>