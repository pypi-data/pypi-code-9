#<ImportSpecificModules>
import sys
BaseModuleStr="ShareYourSystem.Standards.Objects.Initiator")
DecorationModule=BaseModule
#</ImportSpecificModules>


#<DefineFunctions>
def getClassStrWithNameStr(_Str):
	return _Str+"Class"
def getNameStrWithClassStr(_ClassStr):
	return 'Class'.join(_ClassStr.split('Class')[:-1])
def getNameStrWithModuleStr(__ModuleStr):
	return __ModuleStr.split('.')[-1]
#</DefineFunctions>

#<DefineLocals>
BaseNameStr=getNameStrWithModuleStr(BaseModule.__name__)
BaseClass=getattr(BaseModule,getClassStrWithNameStr(BaseNameStr))
#DecorationNameStr=getNameStrWithModuleStr(DecorationModule.__name__)
#DecorationClass=getattr(DecorationModule,getClassStrWithNameStr(DecorationNameStr))
ClassingDecorationStr="Cls@"
#</DefineLocals>

#<DefineClass>
#@DecorationClass
class ClassorClass(BaseClass):

	def default_init(self,**_KwargVariablesDict):

		'''
		#<DefineSpecificDo>
		self.ClassingClass=None
		self.ClassedModule=None
		self.NameStr=""
		#</DefineSpecificDo>
		'''

		#Call the parent init method
		BaseClass.__init__(self,**_KwargVariablesDict)

	def __call__(self,_Class):

		#Do
		self._class(_Class)

		#Return 
		return _Class

	def _class(self,_Class):

		#set
		'''
		if self.ClassingClass==None:
			self.ClassingClass=_Class
			self.ClassedModule=sys.modules[_Class.__module__]

		#set the classed Str of the derived or not classor
		self.NameStr=getNameStrWithClassStr(self.__class__.__name__)
		'''

		#set in the class the classed Strs
		_Class.NameStr=getNameStrWithClassStr(_Class.__name__)

		#Give a Pointer to the Hooker
		setattr(_Class,self.NameStr+'Pointer',self)
		
		#debug 
		'''
		print('Classor l.56 : Give to the SYS')
		print("self.NameStr is ",self.NameStr)
		print('')
		'''

		#Give to the SYS
		#setattr(SYS,self.NameStr,sys.modules[self.__module__])
		#setattr(SYS,self.ClassingClass.__name__,self.ClassingClass)

#</DefineClass>
