# -*- coding: utf-8 -*-
"""


<DefineSource>
@Date : Fri Nov 14 13:20:38 2014 \n
@Author : Erwan Ledoux \n\n
</DefineSource>


An Meteorer maps an append
"""

#<DefineAugmentation>
import ShareYourSystem as SYS
BaseModuleStr="ShareYourSystem.Standards.Controllers.Grider"
DecorationModuleStr="ShareYourSystem.Standards.Classors.Classer"
SYS.setSubModule(globals())
#</DefineAugmentation>

#<ImportSpecificModules>
import ddp
from IPython.display import HTML,display
#</ImportSpecificModules>

#<DefineClass>
@DecorationClass()
class MeteorerClass(BaseClass):
	
	#Definition 
	RepresentingKeyStrsList=[
								'MeteoringWidthInt',
								'MeteoringHeightInt',
								'MeteoringSocketStr',
								'MeteoredConcurrentDDPClientVariable',
								'MeteoredUrlStr',
								'MeteoredHtmlStr',
								'MeteoredHTMLVariable'
							]

	def default_init(self,
						_MeteoringWidthInt=100,
						_MeteoringHeightInt=100,
						_MeteoringSocketStr='ws://127.0.0.1:3000/websocket',
						_MeteoredConcurrentDDPClientVariable=None,
						_MeteoredUrlStr="",
						_MeteoredHtmlStr="",
						_MeteoredHTMLVariable=None,
						**_KwargVariablesDict
				):

		#Call the parent __init__ method
		BaseClass.__init__(self,**_KwargVariablesDict)
		
	def do_meteor(self):

		#Set the MeteoredUrlStr
		self.MeteoredUrlStr='/websocket'.join(
				self.MeteoringSocketStr.split('/websocket')[:-1]
			).replace('ws','http')

		#Do the connection
		self.MeteoredConcurrentDDPClientVariable = ddp.ConcurrentDDPClient(self.MeteoringSocketStr)
		self.MeteoredConcurrentDDPClientVariable.start()
		
		#Init
		"""
		self.MeteoredHtmlStr=""

		#display
		self.MeteoredHtmlStr+="<h1>Client-side</h1><iframe id=\"Client\" width=\""+str(self.MeteoringWidthInt
				)+"\" height=\""+str(self.MeteoringHeightInt
				)+"\" src=\""+self.MeteoredUrlStr+"\" frameborder=\"1\"></iframe>"

		#debug
		'''
		self.debug(('self.',self,[
									'MeteoringUrlStr',
									'MeteoringHeightInt',
									'MeteoringWidthInt',
									'MeteoredHtmlStr'
								]))
		'''

		#Html
		self.MeteoredHTMLVariable=HTML(self.MeteoredHtmlStr)
		
		#display
		display(self.MeteoredHTMLVariable)
		"""

#</DefineClass>
