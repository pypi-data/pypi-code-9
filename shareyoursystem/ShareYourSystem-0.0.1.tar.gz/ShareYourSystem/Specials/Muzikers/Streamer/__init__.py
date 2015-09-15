# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


A Streamer

"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Specials.Muzikers.Muziker"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import music21
#</ImportSpecificModules>

#<DefineLocals>
#</DefineLocals>

#<DefineClass>
@DecorationClass()
class StreamerClass(BaseClass):
	
	#Definition
	RepresentingKeyStrsList=[
								'StreamingNoteStrsList',
								'StreamedMusic21Variable'
							]

	def default_init(self,
						_StreamingNoteStrsList=True,
						_StreamedMusic21Variable='4',
						**_KwargVariablesDict
					):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def do_stream(self):

		#init
		self.StreamedMusic21Variable=music21.stream.Stream()

		#map
		map(
			lambda __StreamingNoteStr:
			self.StreamedMusic21Variable.append(
				music21.note.Note(__StreamingNoteStr)
			),
			self.StreamingNoteStrsList
			)

#</DefineClass>
