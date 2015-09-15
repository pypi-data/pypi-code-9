# ImportModules
import ShareYourSystem as SYS

#Definition a debugging make class
@SYS.DoerClass()
class MakerClass(SYS.DebuggerClass):

	def make1(self):

		#debug
		self.debug('I am in the make1 method')

		#Call the make2 method
		self.make2()

		#debug
		self.debug('I am back in the make1 method')

	def make2(self):

		#debug
		self.debug('I am in the make2 method')

		#Call the make3 method
		self.make3()

		#debug
		self.debug('I am back in the make2 method')

	def make3(self):

		#debug
		self.debug('I am in the make3 method')

		#Call the make4 method
		self.make4()

	def make4(self):

		#debug
		self.debug('I am in the make4 method')

		#debug
		self.debug('I am still in the make4 method')

#Call the make1
MyMaker=MakerClass()
MyMaker.MyTagStr="MyMaker"
MyMaker.make1()

#Call the make1 but with also showing the frame of the argumentinf function
MyMaker.DebuggingNotFrameFunctionStrsList=[]
MyMaker.make1()
